import os
import re
import send2trash
import livemaker_ext
import livemaker_ins
import sys
import subprocess
from pathlib import Path
import traceback

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6 import QtGui

# TODO - 2단계하고 3단계를 바꾸고 싶어요. 인코딩변환을 먼저 하지 않고 원문을 그대로 추출하면, 추출하는 원문에 어떠한 손상도 없다는 게 장점임.
# 원문 위치를 저장하는 알고리즘을 만들어내면 가능하지 않을까요. - 함.
# TODO - 이지트랜스 번역기 32비트짜리 .exe로 만들기., 번역 버튼 만들기.


def resource_path(
    relative_path,
):  # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    # """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


icon = resource_path("WD.ico")
form = resource_path("main.ui")  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결


class livemaker(QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(self, parent, text, ff):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        if ff == None:  # 작업폴더를 설정하지 않았을 경우
            print("작업폴더를 설정하세요")
            return "off"
        self.folder = ff
        self.exe_game = Path(self.folder) / "game.exe"  # 경로 생성
        self.text = text
        self.output = Path(self.folder) / "Output"
        self.workpr = Path.cwd()
        self.a = None
        self.flag = 0
        self.detect()
        print("현재 게임 파일 경로:" + str(self.exe_game))

    def detect(self):
        print("게임 파일명을 찾습니다.")
        list1 = list(Path(self.folder).iterdir())
        if ("game.dat" not in list1) and ("game.ext" not in list1):
            # game.dat, game.ext가 있는지 감지.
            # dat 파일이 없다면 exe 파일 안에 통짜로 되어 있다는 말이니까.
            for e in list1:
                e1 = e.name  # 파일 이름만 가져옴.
                if (
                    (".exe" in e1)
                    and ("ToolForLiveMaker.exe" != e1)
                    and ("_pure.exe" not in e1)
                    and ("_pure_h.exe" not in e1)
                    and ("_new.exe" not in e1)
                    and ("ToolForLiveMakerGUI.exe" != e1)
                ):  # 기존 작업 파일 제외
                    self.exe_game = e  # game.exe에서 감지된 게임 실행경로로 바꿈.
        else:
            print("게임파일이 분할되어 있다는 것을 감지했습니다.")  # game.dat, game.ext가 있을 때.
            self.flag = 1

    def run(self):
        if self.text == "unpack":
            # 빈 폴더에 툴포라이브메이커GUI와 툴포라이브메이커.exe 그리고 원본 게임파일, Hanja.txt, Hanja(restoration).txt만 있다고 할 때.
            # 원본 게임 파일이 dat 파일로 분해된 형식인지, 그냥 exe 파일인지 감지. - detect함수에서 이미 감지함.
            if self.flag == 1:
                list1 = list(Path(self.folder).iterdir())
                if ("game.dat" in list1) and ("game.ext" in list1):
                    # game.dat, game.ext가 있는지 감지.
                    game_list = self.folder + "/game.dat"
                    game_list2 = 0
                    for li in list1:
                        if re.search("game\.[0-9]{3}", li):
                            game_list = game_list + " + " + li
                            game_list2 += 1
                    if game_list2 != 0:  # game.001,game.002 같은 파일이 없을 경우 파일 합치지 않음.
                        folder2 = self.folder + "/game_merged.dat"
                        os.system("copy /b " + game_list + " " + folder2)
                        # dat 파일 합치기.
                        for li in game_list2:  # 번역 합쳤으면, 파일 삭제
                            send2trash.send2trash(li)
                        os.rename("game_merged.dat", "game.dat")  # 파일 이름 바꾸기.

                else:
                    print("game.dat이 없네요. 이상한 게임입니다. 정지합니다.")
                    return

            print("언팩하려는 게임 파일 경로:" + str(self.exe_game))
            im = ["ToolForLiveMaker.exe", "-x", str(self.exe_game), str(self.output)]
            self.a = subprocess.Popen(im)
            self.a.wait()
            self.a.kill()
            print("언팩 성공")

            # Popen 상태 확인 참고 링크, https://stackoverflow.com/questions/14043030/checking-status-of-process-with-subprocess-popen-in-python
        if self.text == "locale":
            if self.flag == 0:
                # dat 파일이 없다면 통짜 exe 파일이니까. - 언팩과정에서 exe파일과 아웃풋 폴더가 분리되어 나왔을 것. pure가 붙은 exe를 로케일해야함.
                self.exe_game = str(self.exe_game).replace(".exe", "_pure.exe")
            im = ["ToolForLiveMaker.exe", "-cvte", str(self.exe_game)]
            self.a = subprocess.Popen(im)

            self.a.wait()
            self.a.kill()
            print("exe 한국어 인코딩 변환 완료")
            im = ["ToolForLiveMaker.exe", "-cvt", str(self.output)]
            self.a = subprocess.Popen(im)
            self.a.wait()
            self.a.kill()

            print("Output 한국어 변환 완료")

        if self.text == "extract":
            if len(list(self.output.glob("**/*.ext.txt"))) == 0:
                # esb 파일이 추출되지 않았을 때에만 실행.
                print("esb 파일을 txt 파일로 변환합니다.")
                im = ["ToolForLiveMaker.exe", "-e   xtt", str(self.output)]
                # 이지트랜스로 번역
                self.a = subprocess.Popen(im)
                self.a.wait()
                self.a.kill()

            try:
                livemaker_ext.main(Path(self.folder))  # 텍스트 추출 코드 실행
            except FileNotFoundError as e:
                print("Output 폴더를 찾을 수 없음" + str(e))
                myWindow.folder1 = None  # 폴더 경로 초기화
                return
            except Exception as e:
                print("ext.txt, tsv 파일 텍스트 추출 중에 TooloflivemakerGUI에러발생:" + str(e))
                print(traceback.format_exc())
                return
            print("추출성공")

        if self.text == "trans":
            im = ["eztrans_call.exe", str(self.output)]
            self.a = subprocess.Popen(im)  # esb에다 텍스트 삽입.
            self.a.wait()
            self.a.kill()

        if self.text == "insert":
            try:
                livemaker_ins.main(Path(self.folder))
            except FileNotFoundError as e:
                print("Output 폴더를 찾을 수 없음" + str(e))
                myWindow.folder1 = None  # 폴더 경로 초기화
                return
            except Exception as e:
                print("ext.txt, tsv 파일에 번역문 삽입 중에 TooloflivemakerGUI에러발생:" + str(e))
                print(traceback.format_exc())
                return
            im = ["ToolForLiveMaker.exe", "-rept", str(self.output)]
            self.a = subprocess.Popen(im)  # esb에다 텍스트 삽입.
            self.a.wait()
            self.a.kill()

        if self.text == "repack":
            j = myWindow.comboBox.currentIndex()  # 콤보박스 값 불러옴.
            for path, dirs, files in os.walk(self.output):  # 추출한 텍스트 파일 삭제
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
                im = [
                    "ToolForLiveMaker.exe",
                    "-p",
                    "--onto",
                    str(self.exe_game),
                    str(self.output),
                ]
                self.a = subprocess.Popen(im)
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p --onto '+self.exe_game+' Output')#exe
            if j == 1:
                im = ["ToolForLiveMaker.exe", "-p", str(self.output)]
                self.a = subprocess.Popen(im)
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p Output')#dat
            if j == 2:
                im = [
                    "ToolForLiveMaker.exe",
                    "-p",
                    "--onto",
                    str(self.exe_game),
                    str(self.output),
                    "-LowVer",
                ]
                self.a = subprocess.Popen(im)
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p --onto '+self.exe_game+' Output -LowVer')
            if j == 3:
                im = ["ToolForLiveMaker.exe", "-p", str(self.output), "-LowVer"]
                self.a = subprocess.Popen(im)
                self.a.wait()
                self.a.kill()
                # os.system('ToolForLiveMaker.exe -p Output -LowVer')
        self.__del__()

    def __del__(self):
        print("프로세스 종료")


# 화면을 띄우는데 사용할 class
class mainWindow(QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.wantachi.clicked.connect(self.wantachi1)
        self.unpack.clicked.connect(self.unpack1)
        self.trans.clicked.connect(self.trans1)
        self.locale.clicked.connect(self.locale1)
        self.extract.clicked.connect(self.extract1)
        self.insert.clicked.connect(self.insert1)
        self.repack.clicked.connect(self.repack1)
        self.setWindowTitle("ToolForLiveMakerGUI 0.2ver")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.folder1 = None

    def livemaker_call(self, commend):
        if self.folder1 == None:  # 게임 폴더 경로를 이용자가 설정하지 않고 버튼을 눌렀다면, 폴더탐색기가 뜨도록.
            self.folder1 = QFileDialog.getExistingDirectory(self, "게임 폴더를 선택하세요")
            if self.folder1 == "":
                print("선택을 취소했습니다.")
                self.folder1 = None
                return
        self.label_4.setText(str(self.folder1))
        a = livemaker(self, commend, self.folder1)  # 게임 이름 전달
        a.start()
        a.wait()

    def unpack1(self):
        self.livemaker_call("unpack")
        self.checkBox.toggle()

    def locale1(self):
        self.livemaker_call("locale")
        self.checkBox_4.toggle()

    def extract1(self):
        self.livemaker_call("extract")
        self.checkBox_2.toggle()

    def trans1(self):
        self.livemaker_call("trans")
        self.checkBox_3.toggle()

    def insert1(self):
        self.livemaker_call("insert")
        self.checkBox_5.toggle()

    def repack1(self):
        self.livemaker_call("repack")
        self.checkBox_6.toggle()

    def wantachi1(self):  # 한번에 3단계까지 이동.
        self.unpack1()
        self.locale1()  # 한국어 인코딩
        self.extract1()  # 스크립트 추출


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    sys.exit(app.exec())
