from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import time
import sys
from multiprocessing import Pool, freeze_support

# from tqdm import tqdm
# from threading import RLock


class TransEngine:
    def initialize(self, engine):
        start = engine.J2K_InitializeEx  # 얘가 함수
        start.argtypes, start.restype = (c_char_p, c_char_p), BOOL

        trans = engine.J2K_TranslateMMNTW  # 얘도 함수
        trans.argtypes, trans.restype = (c_int, c_wchar_p), c_wchar_p
        self.trans = trans

        self.start_obj = start(b"CSUSER123455", b"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\Dat")


try:
    engine_object = WinDLL(r"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngine.dll")
except Exception as e:
    print(str(e).join("\n이지트랜스 설치 경로는 반드시 C:\Program Files (x86)\ChangShinSoft\ezTrans XP\가 돼야 합니다."))
    input()  # 코드 정지용
    sys.exit()

eng = TransEngine()
eng.initialize(engine_object)


def clip_trans(text):  # 클립보드 번역용
    try:
        a = eng.trans(0, "".join(["|:_", text])).lstrip("|:_")
        return a
    except Exception as e:
        return str(e)


def main(a22):  # 텍스트 파일들 번역용, 텍스트 파일 목록만 전달 받도록 함.
    path = Path(a22)
    a23 = (path.parent.joinpath("번역한_텍스트"), path.joinpath("번역한_텍스트"))
    if path.is_file():  # 파일을 넣었을 시
        a24, save_path1 = [path], a23[0]
        save_path1.mkdir(exist_ok=True)
    else:  # 폴더를 넣었을 시
        a24, save_path1 = list(path.glob("**/*.txt")), a23[1]
        try:
            save_path1.mkdir()
        except FileExistsError:
            print("번역한 텍스트가 이미 있는 것 같습니다. 덮어씁니다")
            a24 = [s for s in a24 if "\\번역한_텍스트\\" not in str(s)]

    start_time = time.perf_counter()  # 시간 재기.
    # 저장할 파일 경로 생성
    save_paths = ["".join([str(save_path1 / txt_path.stem), "_번역.txt"]) for txt_path in a24]

    def readfile(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def writefile(save_path, txts):
        with open(save_path, "w", encoding="utf-8") as f:
            f.writelines(txts.get())

    # (ProcessPoolExecutor)을 못 쓴다. eztarans J2KEngine.dll이 락이 걸려서 그런 것 같다.
    """
    https://github.com/tqdm/tqdm/blob/master/examples/parallel_bars.py - 참고
    tqdm.set_lock(RLock())
    p = Pool(initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    p.map(partial(progresser, progress=True), L)
    """

    with Pool() as pool, ThreadPoolExecutor() as thread:
        for texts, file_path in zip(thread.map(readfile, a24), save_paths):  # thread.map으로 파일을 읽어오고 save_paths순으로 텍스트덩어리가 나열됨.
            thread.submit(writefile, file_path, pool.map_async(clip_trans, texts, chunksize=None))
            # thread에게 일거리를 줌. writefile로 파일 경로와 번역한 텍스트들을 줄테니까 저장하라고. 이때, pool.map으로 텍스트들을 멀티프로세스 방식으로 번역함.
            # 파일 읽고 쓰기, 멀티프로세스 작업 할당이 비동기로 움직여 작업속도가 더 빨라질 것이라 예상됨. 아님 말고.

    # print("번역 완료")
    end_time = time.perf_counter()
    print(f"번역한 시간 : {int(round((end_time - start_time) * 1000))}ms")


if __name__ == "__main__":
    freeze_support()
    print("Qootrans ver.0.3 !@!번역할 텍스트는 utf-8 인코딩, .txt 확장자여야 합니다!@!")

    if len(sys.argv) == 1:
        # 인자가 없으면 실행됨.
        print("call_eztrans file_mode (원문 폴더 경로) <-이런 식으로 입력")
        main(r"C:\Users\nsoop\Desktop\workingfolder_current\JPtoKR_Tools\Qootranslator\GUI.ver\새 폴더")
        # 05/01 속도 테스트 용 - 303kb로 실험. - 15557ms - 15.55초
        # // 05/03 - 15242ms - 15.24초 2차 테스트 - 15052msms - 15.05초
        # 3차 테스트 - 14773ms - 14.77초 4차 테스트 - 14487ms - 14.48초(imap씀)
        # 5차 테스트 - 14287ms - 14.28초(비동기 방식 map_async) 6차 테스트 - 14395ms - 14.39초(chunksize=1) 14797ms - 14.79초(chunksize=24)
        # 14351ms - 14.35초(clip_trans 함수 원래대로 함.) 75480ms - 75.48초(chunksize=100000)
        # 15557ms에서 14287ms로 줄었으니 8.2% 정도 빨라짐.
        # 대량으로 번역했을 때 테스트 필요. - 7.47mb로 실험. 기존 코드: 249633ms-24.96초   // 0503 11:30 코드(map사용) - 253220ms - 253.22초// 13:18 코드(map_async사용) - 228720ms - 228.72초//13:27 코드(imap사용) - 231317ms - 231.32초
        # 249633ms에서 228720ms로 줄었으니 8.4% 정도 빨라짐.
        input()  # 코드 정지용
        sys.exit()

    else:
        # 인자가 있으면 실행.
        argv1, argv2 = sys.argv[1], sys.argv[2]
        if argv1 == "clip_mode":
            while argv2 != "exit":
                print(clip_trans(argv2))
                argv2 = input()
        elif argv1 == "file_mode":
            main(argv2)

            # todo: queue를 이용해 반환값을 방출하기.
        else:
            print("인자가 잘못되었습니다.")
            input()  # 코드 정지용
            sys.exit()
    """
    # 파이썬 32비트 버전에서만 됩니다. - 이 때문에 64비트 파이썬에서 쓰려면 exe를 만들어 외부로 빼야할 듯.
    # 출처
    # https://github.com/HelloKS/ezTransWeb

    # 테스트해보니, 몇백개의 텍스트 파일을 작업하는 데 시간이 더럽게 오래걸림.
    # 병렬처리로 만들어야겠음. - 긴가민가했지만, 멀티쓰레드가 안 됨(ThreadPoolExecutor로 됨.). 멀티프로세스로 시도.
    # enhd 적용 확인. - 그러나 때때로 적용이 안되는 경우가 있음. 원인을 모르겠다.
    # 버그 1 - 문자열 맨 앞에 전각 공백'　', 그냥 공백' '이 있는 경우 알아서 생략이 되서 출력. - 문자열 중간에 공백이 있어도 마찬가지.
    # 버그 2 - 때때로 ehnd가 이상하게 적용되는 경우가 있음. - |:_  넣어서 해결. - 아직 완벽하진 않음.
    # 리스트 컴프리헨션을 쓴 경우 - 번역에 든 시간 : 0:00:51.382579
    # 그냥 for문 쓴 경우 - 번역에 든 시간 : 0:00:51.369040
    # 다 때려치고 for문만 주구장창 쓰는 거로.

    번역 부분 속도 테스트 - 멀티쓰레드로도 속도 개선이 있음.
    # ThreadPoolExecutor(max_workers=1)로 번역했을 경우 - 54013ms - 54초
    # ThreadPoolExecutor(max_workers=4)로 번역했을 경우 - 13485ms - 13.5초
    # ThreadPoolExecutor(max_workers=6)로 번역했을 경우 - 10286ms - 10초 - 멀티쓰레드에서 최적값
    # ThreadPoolExecutor(max_workers=8)로 번역했을 경우 - 12022ms - 12초
    # ThreadPoolExecutor(max_workers=12)로 번역했을 경우 - 19969ms - 20초
    # ThreadPoolExecutor(max_workers=16)로 번역했을 경우 - 26469ms  - 26초
    # multiprocessing.Pool()로 번역했을 경우 - 6517ms - 6.5초 - 최적값(번역할 파일이 많을수록 더 빠름.)
    # multiprocessing.Pool(4)로 번역했을 경우 - 11151ms - 11초
    
    # 이번에 개선한 점
            # 1.번역할 파일 읽기 속도, 번역된 파일 저장 속도 개선.
            # 2.텍스트 번역 속도 개선.
            # 기존 방법. 파일 하나 읽고 그 파일의 텍스트를 멀티프로세스로 번역하고 저장하고. 그리고 다음 파일 읽고 번역하고 저장하고. 이런 식.
            # 개선 방법. 여러 텍스트 파일을 한꺼번에 빠르게 읽고 그걸 프로세스풀에 던짐. 그리고 프로세스들은 그걸 하나씩 꺼내서 작업함. 그리고 다시 저장.
            # map_async 비동기 프로그래밍은 어떨까. 더 빠를까? - 더 빠름.
            # 또, chunksize를 크게 하면 더 빠를까? - 1로 해본 결과 더 느림(14395ms).
            # 그리고 프로세스 풀 안에 멀티쓰레드를 하면 어떨까? - 안됨.
    """
