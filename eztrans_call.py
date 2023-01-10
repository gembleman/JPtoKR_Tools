from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL


class TransEngine:
    def initialize(self, engine):
        self.start = engine.J2K_InitializeEx  # 얘가 함수
        self.start.argtypes = [c_char_p, c_char_p]
        self.start.restype = BOOL

        self.trans = engine.J2K_TranslateMMNTW  # 얘도 함수
        self.trans.argtypes = [c_int, c_wchar_p]
        self.trans.restype = c_wchar_p

        self.start_obj = self.start(
            b"CSUSER123455", b"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\Dat"
        )

    def translate_j2k(self, src_text):
        trans_obj = self.trans(0, src_text)
        return trans_obj


engine_object = WinDLL("C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngineH.dll")
eng = TransEngine()
eng.initialize(engine_object)
a = eng.translate_j2k("ポンポン")#테스트 문자열 입력 부문.
#파이썬 32비트 버전에서만 됩니다.
#출처
#https://github.com/HelloKS/ezTransWeb

print(a)
