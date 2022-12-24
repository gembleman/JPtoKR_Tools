import os
import re
import send2trash
import livemaker_ext
import livemaker_ins
import sys
import subprocess

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6 import QtGui


def resource_path(
    relative_path,
):  # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


icon = resource_path("WD.ico")
form = resource_path("main.ui")  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결


class livemaker(QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(
        self, parent, text
    ):  # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.exe_game = "game.exe"
        self.text = text
        self.a = None
        self.detect()

    def detect(self):
        list1 = os.listdir()
        if ("game.dat" not in list1) and (
            "game.ext" not in list1
        ):  # game.dat, game.ext가 있는지 감지.
            # dat 파일이 없다면 exe 파일 안에 통짜로 되어 있다는 말이니까.
            for e in list1:
                if (
                    (".exe" in e)
                    and ("ToolForLiveMaker.exe" != e)
                    and ("_pure.exe" not in e)
                    and ("_pure_h.exe" not in e)
                    and ("_new.exe" not in e)
                    and ("ToolForLiveMakerGUI.exe" != e)
                ):  # 기존 작업 파일 제외
                    self.exe_game = e  # game.exe에서 감지된 게임 실행파일명(死月妖花～四月八日～.exe)으로 바꿈.

    def run(self):
        if self.text == "unpack":
            # 빈 폴더에 툴포라이브메이커GUI와 툴포라이브메이커.exe 그리고 원본 게임파일, Hanja.txt, Hanja(restoration).txt만 있다고 할 때.
            # 원본 게임 파일이 dat 파일로 분해된 형식인지, 그냥 exe 파일인지 감지.
            list1 = os.listdir()
            if ("game.dat" in list1) and (
                "game.ext" in list1
            ):  # game.dat, game.ext가 있는지 감지.
                game_list = "game.dat"
                game_list2 = []
                for li in list1:
                    hu = re.search("game\.[0-9]{3}", li)
                    if hu != None:
                        game_list = game_list + "+" + hu.group()
                        game_list2.append(hu)
                if len(game_list2) != 0:  # game.001,game.002 같은 파일이 없을 경우 이 줄은 넘어간다.
                    os.system(
                        "copy /b " + game_list + " game_merged.dat"
                    )  # dat 파일 합치기.
                    for li in game_list2:  # 번역 합쳤으면, 파일 삭제
                        send2trash.send2trash(li)
                    os.rename("game_merged.dat", "game.dat")  # 파일 이름 바꾸기.
                self.exe_game = "game.exe"
            print("감지된 게임 파일 이름:" + self.exe_game)
            im = "ToolForLiveMaker.exe -x " + self.exe_game + " Output"
            # universal_newlines=True, encoding="utf-8", errors="surrogatepass"
            # universal_newlines=True

            self.a = subprocess.Popen(im, bufsize=0, shell=True)

            self.a.wait()
            self.a.kill()
            # proc = subprocess.Popen(im, shell = Truestdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
            # print(self.livemaker_info)
            print("언팩 성공")

            # Popen 상태 확인 참고 링크, https://stackoverflow.com/questions/14043030/checking-status-of-process-with-subprocess-popen-in-python
        if self.text == "locale":
            list1 = os.listdir()
            if ("game.dat" not in list1) and (
                "game.ext" not in list1
            ):  # game.dat, game.ext가 있는지 감지.
                # dat 파일이 없다면 통짜 exe 파일이니까.
                self.exe_game = self.exe_game.replace(".exe", "_pure.exe")
            # iu = livemaker2(self)
            # iu.start()
            self.a = subprocess.Popen(
                "ToolForLiveMaker.exe -cvte " + self.exe_game, shell=True
            )
            # self.lazer(a)
            self.a.wait()
            self.a.kill()
            print("exe 한국어 인코딩 변환 완료")

            self.a = subprocess.Popen("ToolForLiveMaker.exe -cvt Output")
            self.a.wait()
            self.a.kill()
            # self.lazer(b)
            # os.system('ToolForLiveMaker.exe -cvte '+self.exe_game)#pure_exe파일 한국어 인코딩으로 전환
            print("Output 한국어 변환 완료")
            # os.system('ToolForLiveMaker.exe -cvt Output')#Output 폴더에 있는 파일들, 한국어 인코딩으로 전환
        if self.text == "extract":
            self.a = subprocess.Popen(
                "ToolForLiveMaker.exe -extt --code -kor Output", shell=True
            )
            self.a.wait()
            self.a.kill()
            # os.system('ToolForLiveMaker.exe -extt --code -kor Output')#lsb 파일 코드를 텍스트로 추출
            try:
                livemaker_ext.main()  # 텍스트 추출 코드 실행
            except Exception as e:
                print("ext.txt, tsv 파일 텍스트 추출 중에 TooloflivemakerGUI에러발생:" + str(e))
                return
            print("추출성공")
        if self.text == "insert":
            try:
                livemaker_ins.main()
            except Exception as e:
                print("ext.txt, tsv 파일에 번역문 삽입 중에 TooloflivemakerGUI에러발생:" + str(e))
                return
            self.a = subprocess.Popen("ToolForLiveMaker.exe -rept Output", shell=True)

            self.a.wait()
            self.a.kill()
            # os.system('ToolForLiveMaker.exe -rept Output')#esb 파일 텍스트 삽입.
        if self.text == "repack":
            j = myWindow.comboBox.currentIndex()
            for path, dirs, files in os.walk("Output"):  # 추출한 텍스트 파일 삭제
                print(path + "폴더에서 추출한 텍스트 파일 삭제 중...\n")
                for file in files:
                    if (
                        ".ext.txt" in file or "_번역.txt" in file
                    ):  # .ext가 붙지 않는 텍스트 파일도 있지만, 혹시 몰라 지우지 않음.
                        self.coll = os.path.join(path, file)
                        send2trash.send2trash(self.coll)
            print("추출한 텍스트 파일 삭제 완료.")
            self.exe_game = self.exe_game.replace(".exe", "_pure_h.exe")  # exe 파일 알맞게.
            if j == 0:
                self.a = subprocess.Popen(
                    "ToolForLiveMaker.exe -p --onto " + self.exe_game + " Output",
                    shell=True,
                )
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p --onto '+self.exe_game+' Output')#exe
            if j == 1:
                self.a = subprocess.Popen("ToolForLiveMaker.exe -p Output", shell=True)
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p Output')#dat
            if j == 2:
                self.a = subprocess.Popen(
                    "ToolForLiveMaker.exe -p --onto "
                    + self.exe_game
                    + " Output -LowVer",
                    shell=True,
                )
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p --onto '+self.exe_game+' Output -LowVer')
            if j == 3:
                self.a = subprocess.Popen(
                    "ToolForLiveMaker.exe -p Output -LowVer", shell=True
                )
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p Output -LowVer')


# 화면을 띄우는데 사용할 class
class mainWindow(QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.wantachi.clicked.connect(self.wantachi1)
        self.unpack.clicked.connect(self.unpack1)
        self.locale.clicked.connect(self.locale1)
        self.extract.clicked.connect(self.extract1)
        self.insert.clicked.connect(self.insert1)
        self.repack.clicked.connect(self.repack1)

        self.setWindowTitle("ToolForLiveMakerGUI 0.1ver")
        self.setWindowIcon(QtGui.QIcon(icon))

    def unpack1(self):
        a = livemaker(self, "unpack")  # 게임 이름 전달
        a.start()
        self.checkBox.toggle()

    def locale1(self):
        a = livemaker(self, "locale")
        a.start()
        self.checkBox_2.toggle()

    def extract1(self):
        a = livemaker(self, "extract")
        a.start()
        self.checkBox_3.toggle()

    def insert1(self):
        a = livemaker(self, "insert")
        a.start()
        self.checkBox_4.toggle()

    def repack1(self):
        a = livemaker(self, "repack")
        a.start()
        self.checkBox_6.toggle()

    def wantachi1(self):  # 한번에 3단계까지 이동.
        f = livemaker(self, "unpack")  # 언팩
        f.start()
        # 사월요화는 파일을 교체해줘야 함.
        self.checkBox.toggle()
        self.locale1()  # 한국어 인코딩
        self.checkBox_2.toggle()
        self.extract1()  # 스크립트 추출
        self.checkBox_3.toggle()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    sys.exit(app.exec())
