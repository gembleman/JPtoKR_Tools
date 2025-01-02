import sys
import json

# import call_eztrans
import ctypes
import win32api, win32gui, win32clipboard, win32con

# import trans_api
from pathlib import Path

# import multiprocessing
# import threading
from PyQt6 import QtWidgets, QtCore, QtGui, uic


def resource_path(relative_path):
    # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    # """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return base_path / Path(relative_path)


icon = str(resource_path("Qoo.ico"))
form = str(resource_path("qoo.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결
form2 = str(resource_path("clipwindow.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class2 = uic.loadUiType(form2)[0]  # ui 파일 연결
form3 = str(resource_path("apiwindow.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class3 = uic.loadUiType(form3)[0]  # ui 파일 연결


# qt쓰레드 영역 시작.
# https://abdus.dev/posts/monitor-clipboard/
# qthread를 다시 짜보기로 함. - 0430 - 클립보드 감시자는 qthread 쓰지 않기로 함. 종료가 안됨. - 프로세스 하나 더 만들어서 해결.(다만, 느림.)
# 멀티프로세스로 해결하는 건 폐기. 그냥 qthread 써서 버튼 클릭에 따라 텍스트 표시 여부를 결정하도록 함. - 그러니까. qthread는 계속 돌아가고 있다는 얘기.


# class Clipboard_Watch(QtCore.QThread): 안 씀.
class Clipboard_Watch(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)  # 반드시 클래스 변수로 선언할 것

    def __init__(self):
        super().__init__()
        hwnd = self._create_window()
        ctypes.windll.user32.AddClipboardFormatListener(hwnd)

    def _create_window(self) -> int:
        """
        Create a window for listening to messages
        :return: window hwnd
        """
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._process_message
        wc.lpszClassName = self.__class__.__name__
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)  # 단, 한 번만 실행할 수 있음. 때문에 클래스를 만들 때마다 실행하면 안됨.
        # 에러 메세지: pywintypes.error: (1410, 'RegisterClass', '클래스가 이미 있습니다.')
        return win32gui.CreateWindow(class_atom, self.__class__.__name__, 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

    def _process_message(self, hwnd: int, msg: int, wparam: int, lparam: int):
        WM_CLIPBOARDUPDATE = 0x031D
        if msg == WM_CLIPBOARDUPDATE:
            # 여기가 출력하는 부분.- 가장 중요!!!!
            text = self.read_clipboard()
            if not text:
                return
            # print(text)
            self.signal.emit(text)  # 시그널 발생
        return 0

    @staticmethod
    def read_clipboard():
        try:
            win32clipboard.OpenClipboard()

            def get_formatted(fmt):
                if win32clipboard.IsClipboardFormatAvailable(fmt):
                    return win32clipboard.GetClipboardData(fmt)
                return None

            if text := get_formatted(win32con.CF_UNICODETEXT):
                return text

            return None
        finally:
            win32clipboard.CloseClipboard()

    def run(self):
        print("클립보드 프로세스 시작")
        win32gui.PumpMessages()  # 얘가 무한 반복. - 어떻게 멈추는지 모르겠음.# win32gui.PumpWaitingMessages()
        # 프로세스로 분리해서 종료시킴. 근데 이러면 느림. Q쓰레드를 쓰되, 클립보드 텍스트를 출력하지 않으면 될 듯.


class Qootrans(QtCore.QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(self, folder_path):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__()
        self.a22 = list(set(folder_path))  # 중복 제거.

    def run(self):
        pass
        # trans_api.main(self.a22)

    def stop(self):
        print("프로세스 종료")
        self.quit()
        self.wait(5000)  # 5000ms = 5s


# qt쓰레드 영역 끝.


class clipwindow(QtWidgets.QMainWindow, form_class2):  # 클립보드를 번역한 텍스트를 보여주는 창
    # signal2 = QtCore.pyqtSignal()  # 반드시 클래스 변수로 선언할 것

    # 커스텀 시그널 https://marinelifeirony.tistory.com/81
    def __init__(self, font, stat):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("번역된 텍스트")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.textEdit.setCurrentFont(font)
        # self.label.setText("번역된 텍스트가 여기에 표시됩니다.")
        self.stat = stat  # 버튼 클릭 여부를 저장하는 변수

    # customFunc에서 emit 메서드 실행시 GUI에서 받음.
    @QtCore.pyqtSlot(str)
    def update_text(self, text):
        if self.stat == True:
            self.textEdit.setPlainText(text)

    def closeEvent(self, event):
        # self.signal2.emit()  # 쓰레드 일시정지 보내는 신호- 안 하면 안 꺼지고 돌아가고 있음..(실패 폐기)
        print("클립보드 창 종료")
        self.stat = False


class apiwindow(QtWidgets.QMainWindow, form_class3):  # API키 입력하는 창
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
                self.item = QtWidgets.QListWidgetItem("API키 입력")  # 엔터 키가 눌렸을 때, 추가되는 아이템.
                self.item.setFlags(self.item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                self.currentwidget.addItem(self.item)
                self.currentwidget.setCurrentItem(self.item)
                self.currentwidget.editItem(self.item)  # self.listWidget<-위젯 값이 달라지면, 그 값에 맞는 위젯을 호출시킴 그리고 그 위젯에 item을 추가시킴

    def closeEvent(self, event):
        print(myWindow.setting)
        api_keys_dic = {"papago_free_api": {}, "papago_paid_api": {}, "deepL_api": [], "google_api": []}  #
        # 파파고 요금 좀 낮춰주세요.
        myWindow.setting["api_keys"] = {}  # api키를 저장하는 딕셔너리를 초기화시킨다.

        # papago 오픈api 키나 pro키나 똑같은 입력창에 입력하도록 만들기. 굳이 따로 나눌 필요 없음. 프로그램이 알아서 인식하게 만들면 됨.
        # 무료키는 무조건 id는 20글자, secret는 10글자. 유료키는 id는 10글자, secret은 40글자.
        for n in range(self.listWidget_7.count()):  # papago_api용_cilent ID
            papago_cilent_id = self.listWidget_7.item(n).text()
            try:
                papago_secret = self.listWidget_8.item(n).text()
            except:
                print("Secret을 입력하지 않았어요.")
                continue
            if papago_cilent_id in ["API키 입력", "ID 입력"] or papago_secret in ["API키 입력", "Secret 입력"]:
                print("ID나 Secret을 입력하지 않았어요.")
                continue

            if len(papago_cilent_id) == 20 and len(papago_secret) == 10:
                api_keys_dic["papago_free_api"][papago_cilent_id] = papago_secret
            elif len(papago_cilent_id) == 10 and len(papago_secret) == 40:
                api_keys_dic["papago_paid_api"][papago_cilent_id] = papago_secret
            else:
                print("파파고 api키가 아니에요, 다시 입력해주세요")
                continue

        for n in range(self.listWidget_5.count()):  # deepL_api용
            deepL_key = self.listWidget_5.item(n).text()
            if deepL_key == "API키 입력":
                continue
            print(deepL_key)
            api_keys_dic["deepL_api"].append(deepL_key)

        for n in range(self.listWidget_6.count()):  # google_api용
            google_key = self.listWidget_6.item(n).text()
            if google_key in ["API키 입력", "유료 API키를 적어주세요. 무료 버전이 작동하지 않으면 쓰입니다."]:
                continue
            print(google_key)
            api_keys_dic["google_api"].append(google_key)

        myWindow.setting["api_keys"] = api_keys_dic

        print("창 닫힘")


# 화면을 띄우는데 사용할 class
class mainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.groupBox_2.setVisible(False)
        self.apiButton.setVisible(False)
        self.trans_button.clicked.connect(self.file_trans)
        self.comboBox_2.currentIndexChanged.connect(self.combo)
        self.comboBox_6.currentIndexChanged.connect(self.set_targetlang)
        self.apiButton.clicked.connect(self.openapi)
        self.clipButton.clicked.connect(self.clipwindow)
        self.pushButton.clicked.connect(self.fontwindow)

        self.setWindowTitle("QooTranslator")
        self.setWindowIcon(QtGui.QIcon(icon))
        self.folder1 = None
        self.folder2 = []
        self.api = None
        self.worker_thread = None
        self.clipboard = None
        self.clip = None
        self.stat = True
        self.font = QtGui.QFont("Arial", 10)
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

        # 파파고용_언어 목록
        # fmt: off
        self.papago_source = ["일본어", "한국어", "영어", "중국어 간체", "중국어 번체", "베트남어", "인도네시아어", "태국어", "독일어", "러시아어", "스페인어", "이탈리아어", "프랑스어"]
        self.papago_target = {"한국어": ["영어", "일본어", "중국어 간체", "중국어 번체", "베트남어", "인도네시아어", "태국어", "독일어", "러시아어", "스페인어", "이탈리아어", "프랑스어"],
                              "일본어": ["한국어", "영어", "중국어 간체", "중국어 번체"],
                              "영어": ["일본어", "프랑스어", "중국어 간체", "중국어 번체", "한국어"],
                              "중국어 간체": ["중국어 번체", "한국어", "일본어", "영어"],
                              "중국어 번체": ["중국어 간체", "한국어", "일본어", "영어"],
                              "베트남어": ["한국어"], "인도네시아어": ["한국어"],
                              "태국어": ["한국어"], "독일어": ["한국어"], "러시아어": ["한국어"],
                              "스페인어": ["한국어"], "이탈리아어": ["한국어"], "프랑스어": ["한국어", "영어"]}
        self.deepL_langs = ["자동감지","한국어", "일본어", "영어", "중국어", "불가리아어", "체코어","덴마크어","독일어","그리스어","스페인어","에스토니아어","핀란드어","프랑스어","헝가리어",
                            "인도네시아어","이탈리아어","리투아니아어","라트비아어","노르웨이어","네덜란드어","폴란드어","포르투갈어","루마니아어","러시아어","슬로바키아어",
                            "슬로베니아어","스웨덴어","터키어","우크라이나어"]
        self.google_langs = ["자동감지","한국어","일본어","영어","중국어 간체", "중국어 번체","포르투갈어", "스페인어", "프랑스어", "독일어", "베트남어", "튀르키예어",
                             "아프리칸스어","알바니아어","암하라어","아랍어","아르메니아어","아제르바이잔어","밤바라어","바스크어","벨라루스어",
                             "벵골어","보지푸리어","불가리아어","카탈루냐어","세부아노어", "코르시카어","크로아티아어","체코어","덴마크어","디베히어","도그리어","네덜란드어","에스페란토어",
                             "에스토니아어","에웨어","필리핀어","프리지아어","갈리시아어","조지아어","그리스어","과라니아어","구자라트어","아이티크리올어","하우사어","하와이어","히브리어",
                             "힌디어","몽어","헝가리어","아이슬란드어","이보어","일로카노어","인도네시아어","아일랜드어","자바어","칸나디어","카자흐어","크메르어","키냐르완다어","콘칸어","크리오어",
                             "쿠르드어","소라니어","키르기스어","라오어","라틴어","라트비아어","링갈라어","리투아니아어","루간다어","룩셈베르크어","마케도니아어","마이틸리어","말라가시어","말레이어",
                             "말라얄람어","몰타어","마오리어","마라티어","메이테이어","미조어","몽골어","미얀마어","네팔어","노르웨이어","니안자어","오리야어","오로모어","파슈토어","페르시아어",
                             "폴란드어","펀자브어","케추아어","루마니아어","러시아어","사모아어","산스크리트어","게일어","북소토어","세르비아어","세소토어","쇼나어","신디어",
                             "스리랑카어","슬로바키아어","슬로베니아어","소말리어","순다어","스와힐리어","스웨덴어","필리핀어","타지크어","타밀어","타타르어","텔루구어","태국어","티그리냐어",
                             "총가어","투르크멘어","트위어","우크라이나어","우르두어","위구르어","우즈베크어","웨일즈어","코사어","이디시어","요루바어","줄루어"]
        # fmt: on

    def clipwindow(self):  # 클립보드를 번역한 텍스트를 보여주는 창
        self.stat = True
        self.clip = clipwindow(self.font, self.stat)  # 버튼을 누를 때마다 매번 새로 갱신됨.
        if self.clipboard == None:
            self.clipboard = Clipboard_Watch()
        if self.worker_thread == None:
            self.worker_thread = QtCore.QThread()
            self.clipboard.moveToThread(self.worker_thread)
            self.worker_thread.start()
        self.clipboard.signal.connect(self.clip.update_text)
        # self.clip.signal2.connect(self.clipboard.stop)
        self.clip.show()

    def openapi(self):  # API키 입력하는 창
        # https://www.pythonguis.com/tutorials/creating-multiple-windows/ - 참고함. - 창을 띄웠다가 닫고 다시 띄우면 이전 창의 메모리가 초기화되버리는 문제 해결.
        if self.api == None:  # 처음에 생성해야 하는 경우를 제외하고 api창을 새로 생성하지 말도록 하면 됨.
            self.api = apiwindow()
        self.api.show()

    def combo(self):  # 콤보박스 선택에 따라서 버튼과 그룹박스를 보이게 하거나 안보이게 한다.
        self.current_index = self.comboBox_2.currentIndex()
        if self.current_index in [0, 1]:
            self.apiButton.setVisible(False)
            self.groupBox_2.setVisible(False)
            self.label_6.setVisible(True)

        elif self.current_index in [2, 3, 4]:
            self.apiButton.setVisible(True)
            self.groupBox_2.setVisible(True)
            self.label_6.setVisible(False)
            self.comboBox_6.clear()
            self.comboBox_7.clear()
            if self.current_index == 2:  # papago일 때.
                self.comboBox_6.addItems(self.papago_source)
                self.comboBox_7.addItems(self.papago_target["일본어"])
            elif self.current_index == 3:  # deepL일 때.
                self.comboBox_6.addItems(self.deepL_langs)
                self.comboBox_7.addItems(self.deepL_langs)
            elif self.current_index == 4:  # google일 때.
                self.comboBox_6.addItems(self.google_langs)
                self.comboBox_7.addItems(self.google_langs)

    def set_targetlang(self):  # papago일 때, target언어를 설정하는 함수.
        if self.current_index == 2:
            self.current_index2 = self.comboBox_6.currentIndex()
            self.comboBox_7.clear()
            self.comboBox_7.addItems(self.papago_target[self.papago_source[self.current_index2]])

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
                self.listWidget_2.addItem(Path(f).name)  # 경로 전체가 아니라 파일이나 폴더 이름만 넣기.
            elif Path(f).is_file() and Path(f).suffix == ".txt":
                print("번역할 파일 경로: " + f)
                self.folder2.append(f)
                self.listWidget_2.addItem(Path(f).name)
            else:
                print(f + "\n텍스트 파일 및 폴더가 아닙니다...")

    def fontwindow(self):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            print(font)
            self.font = font

    def file_trans(self):  # 파일 번역 시작하는 버튼
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
    # multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    print("쿠우 번역기 ver.0.2 made by gemble\nQuickly Optimized Operations Translator")
    sys.exit(app.exec())

# todo 번역 엔진 콤보 박스 언어 선택지 구현하기.
# todo 로그 파일 mega.nz 업로드 구현하기.
# todo 이지트랜스 32비트 exe만들기. - 이름은 eztrans32_api.exe
# todo 클립보드 번역문 띄우는 창 구현하기.
# 번역 api 구현 - 파파고api는 무료부터 쓰도록, 그 다음은 유료키쓰는 거로.
# 나중에는 후킹까지 구현해서 번역할 수 있도록.
# 쿠우 번역기와 쿠우트랜스는 엄밀히 말해서 다름. 쿠우트랜스는 일한번역 모델임.
