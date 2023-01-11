import os
import re
import send2trash
import pathlib

# import livemaker_ext
# import livemaker_ins
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


class wolfdec(QThread):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.exe_game = "game.exe"
        self.text = text
        self.a = None

    def run(self):
        if self.text == "unpack":
            pass


icon = resource_path("WD.ico")
form = resource_path("main.ui")  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
# form_class = uic.loadUiType(form)[0]  # ui 파일 연결


# 화면을 띄우는데 사용할 class
class mainWindow(QMainWindow, uic.loadUiType(form)[0]):
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

        self.setWindowTitle("WolfDecGUI 0.1ver")
        self.setWindowIcon(QtGui.QIcon(icon))

    def unpack1(self):
        a = wolfdec(self, "unpack")  # 게임 이름 전달
        a.start()
        self.checkBox.toggle()

    def locale1(self):
        a = wolfdec(self, "locale")
        a.start()
        self.checkBox_2.toggle()

    def extract1(self):
        a = wolfdec(self, "extract")
        a.start()
        self.checkBox_3.toggle()

    def insert1(self):
        a = wolfdec(self, "insert")
        a.start()
        self.checkBox_4.toggle()

    def repack1(self):
        a = wolfdec(self, "repack")
        a.start()
        self.checkBox_6.toggle()

    def wantachi1(self):  # 한번에 3단계까지 이동.
        folder = QFileDialog.getExistingDirectory(self, "게임 폴더를 선택하세요")
        print(folder)

        if pathlib.Path(folder + "\Data") == False:
            print("Data폴더가 없습니다. 독특하네요")
            quit()
        if pathlib.Path(folder + "\Game.exe") == False:
            print("폴더 안 Game.exe파일이 감지되지 않습니다. 독특하네요\n일단 폴더 안에 있는 exe파일을 검사합니다.")
            r = list(pathlib.Path(folder).glob(r"*.exe"))
            kill = open(r, "rb")
            kill.read()

        quit()
        f = wolfdec(self, "unpack")  # 언팩
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
