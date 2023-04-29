# from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
# from tqdm import tqdm
# from statistics import mean
import csv

# import pyperclip
# 뭐가 문제인지 모르겠는데, 실시간으로 클립보드 내용을 불러오지 못하더라. - 프로세스 충돌로 추정중. 시간차를 두어서 후커와 이거가 서로 번갈아가며 클립보드에 접근하도록 함.
# 그런데 이렇게 해결했더니, 뭐가 문제냐면 클립보드가 씹힘.
# import time
# import atexit
# from tkinter import Tk
# import win32clipboard

import threading

# import multiprocessing
import ctypes

# from pathlib import Path
import win32api, win32gui, win32clipboard, win32con

# I got the source code from this site.. Thanks.
# https://abdus.dev/posts/monitor-clipboard/


class Clipboard_Watch:
    def _create_window(self) -> int:
        """
        Create a window for listening to messages
        :return: window hwnd
        """
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._process_message
        wc.lpszClassName = self.__class__.__name__
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        return win32gui.CreateWindow(class_atom, self.__class__.__name__, 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

    def _process_message(self, hwnd: int, msg: int, wparam: int, lparam: int):
        WM_CLIPBOARDUPDATE = 0x031D
        if msg == WM_CLIPBOARDUPDATE:
            # 여기가 출력하는 부분.- 가장 중요!!!!
            text = self.read_clipboard()
            if not text:
                return
            print(text)
            pred_text = text
            for pre_token in self.pre_dic.keys():  # 전처리사전 -
                pred_text = pred_text.replace(pre_token, self.pre_dic[pre_token])

            # time.sleep(0.5)
            trans_text = self.trans(pred_text)

            post_text = trans_text
            for pos_token in self.post_dic.keys():  # 후처리사전 -
                post_text = post_text.replace(pos_token, self.post_dic[pos_token])

            self.ss.writerow([text, post_text])  # 번역한 스크립트 저장. - 나중에 이 데이터로 모델 개선할 거임.
            print(post_text)

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

    def listen(self):
        def runner():
            hwnd = self._create_window()
            ctypes.windll.user32.AddClipboardFormatListener(hwnd)  # 클립보드 감시자
            win32gui.PumpMessages()

            th = threading.Thread(target=runner, daemon=True)
            th.start()
            while th.is_alive():
                th.join()


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    clipboard = Clipboard_Watch()
    clipboard.listen()

# 번역하는 부분을 서브프로세스로 돌리고. 클립보드로 받아오는 부분에 병목이 안 생기도록

# time.sleep(0.21)#무조건 해야됨. 클립보드를 쓰는 프로그램이 동시에 두개여선 안됨. 약간의 시간차를 줘야 한다. 0.001은 안됨. 0.01, 0.1도 안됨. - 해결함. 클립보드 감시자로 해결.

# 전처리,후처리 사전 필요. - 후처리만 일단 조잡하게나마 구현. 전처리는 모델을 새로 짜야함. 일단 보류.
# 이용자가 처리하는 텍스트 기록

# 이 아랫부분은 BLEU 점수 측정용. 일단 나중에.
# quit()
"""
bleu = []
f1 = []

DATA_ROOT = 'output'
#FILE_JP_KO_TEST = 'ja_ko_test.csv'
FILE_FFAC_TEST = 'cli2.csv'

with torch.no_grad(), open(f'{DATA_ROOT}/{FILE_FFAC_TEST}', 'r', encoding = 'utf-8') as fd:
# with torch.no_grad(), open(f'{DATA_ROOT}/{FILE_JP_KO_TEST}', 'r') as fd:
    reader = csv.reader(fd)
    next(reader)
    datas = [row for row in reader]    

    for data in tqdm(datas, "Testing"):
        input, label = data
        embeddings = src_tokenizer(input, return_attention_mask=False, return_token_type_ids=False, return_tensors='pt').to(device)
        embeddings = {k: v for k, v in embeddings.items()}
        with torch.no_grad():
            output = model.generate(**embeddings)[0, 1:-1]
        preds = trg_tokenizer.decode(output.cpu())

        bleu.append(sentence_bleu([label.split()], preds.split(), weights=[1,0,0,0], smoothing_function=smoothie))

print(f"Bleu score: {mean(bleu)}")
"""
