import PyQt6
#import webbrowser
import video_ext
from PyQt6 import uic
import sys
import pathlib


def resource_path(relative_path):
    # pyinstall용 ui파일 불러오지 못하는 문제. https://editor752.tistory.com/140
    # """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", pathlib.Path(__file__).resolve().parent)
    return base_path / pathlib.Path(relative_path)


icon = str(resource_path("Voat.ico"))
form = str(resource_path("voat.ui"))  # pyinstall용 ui파일 불러오지 못하는 문제 - 해결용
form_class = uic.loadUiType(form)[0]  # ui 파일 연결


class Voatsub(PyQt6.QtCore.QThread):  # 쓰레드 구현
    # 초기화 메서드 구현
    def __init__(self, parent, file_paths):
        # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.filepaths = file_paths

    def run(self):
        self.method_index = [myWindow.comboBox.currentIndex(),myWindow.comboBox_2.currentIndex()]
        self.call = video_ext.recognizion(self.filepaths,self.method_index,)
        
        self.call.run()
        


class mainWindow(PyQt6.QtWidgets.QMainWindow, form_class):
    def __init__(self):  # 클래스에서 자동 호출 함수
        super().__init__()
        # 아래는 시그널
        self.setupUi(self)
        self.voice_rec1.clicked.connect(self.voice_rec)
        #self.comboBox.currentIndexChanged.connect(self.updateCombo)
        #self.sub_lists = {"whisper":['자동선택','tiny','small','medium','large(권장)',]}

        self.setWindowTitle("VOATgenerator")
        self.setWindowIcon(PyQt6.QtGui.QIcon(icon))
        self.textBrowser.append("보트 자막생성기 ver.0.2 made by gemble\nVOice Analyzing Text Subtitler(VOATsubtitler)\n오디오나 비디오 파일을 넣어주세요\n음성 타이밍이 들어간 .srt 자막 파일도 함께 넣는 것을 권장합니다\n파일들은 여기다 드래그&드롭")
        self.folder1 = None
        self.filedic = {}

        self.one, self.two, self.three = range(3)
        #qtview에 넣을 틀
        self.model = PyQt6.QtGui.QStandardItemModel(0, 3)
        self.model.setHeaderData(self.one, PyQt6.QtCore.Qt.Orientation.Horizontal, "이름")
        self.model.setHeaderData(self.two, PyQt6.QtCore.Qt.Orientation.Horizontal, "자막 여부")
        self.model.setHeaderData(self.three, PyQt6.QtCore.Qt.Orientation.Horizontal, "Type")
        
        self.treeView.setModel(self.model)
        
        #메뉴바 설정
        #self.menu.aboutToShow.connect(self.add_open)
    '''
    def add_open(self):
        self.print2("감사합니다!")
        webbrowser.open("https://toss.me/gemble")
    '''

    def print2(self, line):
        self.textBrowser.append(line)
        #textBrowser
    
    def add_file(self, model, file_name, sub_ox, file_type):
        model.insertRow(0)
        model.setData(model.index(0, self.one), file_name)
        model.setData(model.index(0, self.two), sub_ox)
        model.setData(model.index(0, self.three), file_type)
    
    #파일 포맷에 따라 파일 이름 변하기.
    def format_rec(self, file_paths):
        video_format = [".mkv",".flv",".vob",".ogv",".avi",".mts",".m2ts",".ts",".mov",".wmv",".mp4",".flv",]
        audio_format = [".aac", ".flac", ".m4a", ".mp3", ".opus", ".wav"]
        
        self.file_paths = file_paths
        
        for self.file_path in self.file_paths:
            self.path2 = pathlib.Path(self.file_path)
            if self.path2.is_file():
                self.print2("인식할 파일 경로: " + str(self.path2))
                

                self.path_sub = self.path2.with_suffix('.srt')
                self.file_ext = self.path2.suffix

                if self.file_ext in video_format:
                    self.print2(f"{self.file_ext} 비디오 포맷입니다.")
                    #비디오 파일을 넣으면 자동으로 같은 이름의 자막 파일 넣기.
                    if self.path_sub.exists():
                        #자막 파일이 있으면 이쪽으로 간다.
                        self.filedic[self.file_path] = "video+sub"
                        self.add_file(self.model, self.path2.name, '자막 있음', self.file_ext)
                    else:
                        self.filedic[self.file_path] = "video_only"
                        self.add_file(self.model, self.path2.name, '자막 없음', self.file_ext)
                    

                if self.file_ext in audio_format:
                    self.print2(f"{self.file_ext} 오디오 포맷입니다.")
                    if self.path_sub.exists():
                        #자막 파일이 있으면 이쪽으로 간다.
                        self.filedic[self.file_path] = "audio+sub"
                        self.add_file(self.model, self.path2.name, '자막 있음', self.file_ext)
                    else:
                        self.filedic[self.file_path] = "audio"
                        self.add_file(self.model, self.path2.name, '자막 없음', self.file_ext)
            else:
                self.print2(self.file_path + "\n비디오, 오디오 파일만 넣어주세요")


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.format_rec(self.files)

    def voice_rec(self):
        self.plag = 0
        if self.filedic != {}:
            self.print2("드래그&드롭")
            self.plag = 1
        else:
            if self.folder1 == None:  # 파일 경로를 이용자가 설정하지 않고 버튼을 눌렀다면, 폴더탐색기가 뜨도록.
                self.folder1 = PyQt6.QFileDialog.getOpenFileNames(self, "음성 인식할 파일들을 선택하세요")
                print(self.folder1[0])
                if self.folder1 == "":
                    self.print2("선택을 취소했습니다.")
                    self.folder1 = None
                    return
                else:
                    self.format_rec(self.folder1[0])
                    self.plag = 1
        if self.plag == 1:
            a = Voatsub(self, self.filedic)  # 파일 이름 전달
            a.start()
            a.wait()

            # 타이밍이 할당된 자막 파일을 넣는 것을 권장합니다.
            # 파일들은 여기다 드래그&드롭
            # 음성이나 비디오 파일을 넣어주세요. 이와 대응하는 자막 파일도 넣어주시면 더욱 좋습니다.


if __name__ == "__main__":

    app = PyQt6.QtWidgets.QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()  # 프로그램 창을 띄움
    
    sys.exit(app.exec())
