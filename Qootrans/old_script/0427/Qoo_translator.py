import sys
import json

# import qoo_call
from pathlib import Path
import multiprocessing

from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6 import QtGui


def resource_path(relative_path):
    # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    # """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return base_path / Path(relative_path)


icon = str(resource_path("Qoo.ico"))
form = str(resource_path("qoo.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결
form2 = str(resource_path("txtwindow.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class2 = uic.loadUiType(form2)[0]  # ui 파일 연결
form3 = str(resource_path("apiwindow.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class3 = uic.loadUiType(form3)[0]  # ui 파일 연결


class Qootrans(QtCore.QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(self, parent, folder_path):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.a22 = list(set(folder_path))  # 중복 제거.

    def run(self):
        pass
        # qoo_call.main(self.a22)

    def __del__(self):
        print("프로세스 종료")


class clipwindow(QtWidgets.QMainWindow, form_class2):  # 클립보드를 번역한 텍스트를 보여주는 창
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("번역된 텍스트")


class apiwindow(QtWidgets.QMainWindow, form_class3):  # api키를 입력하는 창
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("API키 입력")
        self.setWindowIcon(QtGui.QIcon(icon))
        # self.listWidget.itemDoubleClicked.connect(self.addapi)

    """
    def addapi(self):
        self.listWidget.openPersistentEditor(self.listWidget.item(0))
        pass
        # qoo_call.addapi(self.lineEdit.text())
    """

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key.Key_Return:
            self.focus = QtWidgets.QApplication.focusWidget().objectName()  # 현재 포커스되어 있는 위젯의 이름을 가져온다.
            self.currentwidget = getattr(self, self.focus)  # 현재 포커스되어 있는 위젯을 가져온다.
            self.currentitem = self.currentwidget.currentItem()

            if self.currentwidget.isPersistentEditorOpen(self.currentitem) == False:
                self.item = QtWidgets.QListWidgetItem("API키를 입력해주세요.")  # 엔터 키가 눌렸을 때, 추가되는 아이템.
                self.item.setFlags(self.item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                self.currentwidget.addItem(self.item)
                self.currentwidget.setCurrentItem(self.item)
                self.currentwidget.editItem(self.item)  # self.listWidget<-위젯 값이 달라지면, 그 값에 맞는 위젯을 호출시킴 그리고 그 위젯에 item을 추가시킴

    def closeEvent(self, event):
        print(myWindow.setting)
        papago_free_api = {"papago_free_api": []}
        papago_paid_api = {"papago_paid_api": []}  # 파파고 요금 좀 낮춰주세요.
        deepL_api = {"deepL_api": []}
        google_api = {"google_api": []}

        for n in range(self.listWidget_1.count()):  # papago_free_api용
            print(self.listWidget_1.item(n).text())
            papago_free_api["papago_free_api"].append(self.listWidget_1.item(n).text())
        myWindow.setting["api_keys"].append(papago_free_api)

        for n in range(self.listWidget_2.count()):  # papago_paid_api용
            print(self.listWidget_2.item(n).text())
            papago_paid_api["papago_paid_api"].append(self.listWidget_2.item(n).text())
        myWindow.setting["api_keys"].append(papago_paid_api)

        for n in range(self.listWidget_3.count()):  # deepL_api용
            print(self.listWidget_3.item(n).text())
            deepL_api["deepL_api"].append(self.listWidget_3.item(n).text())
        myWindow.setting["api_keys"].append(deepL_api)

        for n in range(self.listWidget_4.count()):  # google_api용
            print(self.listWidget_4.item(n).text())
            google_api["google_api"].append(self.listWidget_4.item(n).text())
        myWindow.setting["api_keys"].append(google_api)

        print("닫힘")


# 화면을 띄우는데 사용할 class
class mainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.trans_button.clicked.connect(self.trans1)
        self.groupBox_2.setVisible(False)
        self.apiButton.setVisible(False)
        self.comboBox_2.currentIndexChanged.connect(self.combo)
        self.apiButton.clicked.connect(self.openapi)
        self.clipButton.clicked.connect(self.clipwindow)

        self.setWindowTitle("QooTranslator")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.folder1 = None
        self.folder2 = []

        self.setting = {
            "engine": "",
            "api_keys": [],
            "sorce_lang": "",
            "target_lang": "",
        }
        set_file = Path("setting.json")
        set_file.touch()
        if set_file.stat().st_size != 0:
            with open("setting.json", "r", encoding="utf-8") as f:
                self.setting = json.load(f)

    def clipwindow(self):  # 클립보드를 번역한 텍스트를 보여주는 창
        self.clip = clipwindow()
        self.clip.show()

    def openapi(self):  # api키를 입력하는 창
        self.api = apiwindow()
        self.api.show()

    def combo(self):  # 콤보박스 선택에 따라서 버튼과 그룹박스를 보이게 하거나 안보이게 한다.
        if self.comboBox_2.currentIndex() in [0, 1]:
            self.apiButton.setVisible(False)
            self.groupBox_2.setVisible(False)

        elif self.comboBox_2.currentIndex() in [2, 3, 4]:
            self.apiButton.setVisible(True)
            self.groupBox_2.setVisible(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if Path(f).is_dir():
                print("번역할 폴더 경로: " + f)
                self.folder2.append(f)
                self.listWidget_2.addItem(f)
            elif Path(f).is_file() and Path(f).suffix == ".txt":
                print("번역할 파일 경로: " + f)
                self.folder2.append(f)
                self.listWidget_2.addItem(f)
            else:
                print(f + "\n이건 파일인데...")

    def trans1(self):  # 파일 번역 시작하는 버튼
        if self.folder2 != []:
            print("드래그&드롭")
            for folder in self.folder2:
                a = Qootrans(self, folder)  # 텍스트 이름 전달
                a.start()
                a.wait()
        else:
            if self.folder1 == None:  # 게임 폴더 경로를 이용자가 설정하지 않고 버튼을 눌렀다면, 폴더탐색기가 뜨도록.
                self.folder1 = QtWidgets.QFileDialog.getExistingDirectory(self, "번역할 폴더를 선택하세요")

                if self.folder1 == "":
                    print("선택을 취소했습니다.")
                    self.folder1 = None
                    return
                a = Qootrans(self, self.folder1)
                a.start()

    """
    def cliptrans(self):
        print("클립보드 번역")
        a = Qootrans(self, "clip")
    """

    def closeEvent(self, event):
        print("종료")
        with open("setting.json", "w", encoding="utf-8") as f:
            json.dump(self.setting, f, indent=4, ensure_ascii=False)


# todo 드래그 앤 드롭으로 파일을 끌어다놓을 수 있게 하기.

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    print("쿠우 번역기 ver.0.2 made by gemble\nQuickly Optimized Operations Translator(QooTrans)")
    sys.exit(app.exec())
