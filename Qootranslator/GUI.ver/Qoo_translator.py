import sys
import qoo_call
from pathlib import Path
import multiprocessing

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtGui

def resource_path(relative_path):  
    # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    # """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return base_path / Path(relative_path)


icon = str(resource_path("Qoo.ico"))
form = str(resource_path("qoo.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결


class Qootrans(QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(self, parent, folder_path):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.a22 = folder_path

    def run(self):
        qoo_call.main(self.a22)
        
    def __del__(self):
        print("프로세스 종료")


# 화면을 띄우는데 사용할 class
class mainWindow(QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.trans_button.clicked.connect(self.trans1)

        self.setWindowTitle("QooTranslator")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.folder1 = None
        self.folder2 = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if Path(f).is_dir():
                print('번역할 폴더 경로: '+f)
                self.folder2.append(f)
            else:
                print(f+"\n이건 파일인데...")
        

    def trans1(self):
        if self.folder2 != []:
            print('드래그&드롭')
            for folder in self.folder2:
                a = Qootrans(self,folder)  # 게임 이름 전달
                a.start()
                a.wait()
        else:
            if self.folder1 == None:  # 게임 폴더 경로를 이용자가 설정하지 않고 버튼을 눌렀다면, 폴더탐색기가 뜨도록.
                self.folder1 = QFileDialog.getExistingDirectory(self, "번역할 폴더를 선택하세요")
                if self.folder1 == "":
                    print("선택을 취소했습니다.")
                    self.folder1 = None
                    return
                a = Qootrans(self,self.folder1)  # 게임 이름 전달
                a.start()
        


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    print("쿠우 번역기 ver.0.2 made by gemble\nQuickly Optimized Operations Translator(Qoo Translator)")
    sys.exit(app.exec())
