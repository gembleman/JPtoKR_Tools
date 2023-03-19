import moviepy.editor as mp
from pathlib import Path

from faster_whisper import WhisperModel
import torch
from timedelta import Timedelta
import send2trash
from huggingface_hub import snapshot_download

class recognizion:
    def __init__(self, file_dics, method):
        self.stt_method = method
        self.file_dics = file_dics
        print(file_dics)
        print(method)
        self.video_right = 0
        
        

    def run(self):
        #self.aaa = self.file_dics.keys
        for self.file_path in self.file_dics.keys():
            
            if self.file_dics[self.file_path] == "video+sub":
                print(f"{self.file_path} 비디오와 자막 인식했습니다.")
                #비디오 파일을 넣으면 자동으로 같은 이름의 자막 파일 넣기.
                self.audio_path = self.convert_video_to_audio_ffmpeg(self.file_path)
                self.nym = "sub"#자막 파일을 이용해서 인식해라.
                self.video_right = 1
            
            if self.file_dics[self.file_path] == "video_only":
                print(f"{self.file_path} 비디오 인식했습니다.")
                self.audio_path = self.convert_video_to_audio_ffmpeg(self.file_path)
                self.video_right = 1
                

            if self.file_dics[self.file_path] == "audio":
                print(f"{self.file_path} 오디오 포맷입니다.")
                
                

            #whisper 모델 택했다면 이쪽으로
            if self.stt_method[0] == 0:#whisper-
                if self.stt_method[1] == 0:#whisper-auto
                    self.whisper_exe(language=None, file_path = self.file_path)
                if self.stt_method[1] == 1:#whisper-korean
                    self.whisper_exe(language="ko", file_path = self.audio_path)
                if self.stt_method[1] == 2:#whisper-english
                    self.whisper_exe(language="en", file_path = self.audio_path)
                if self.stt_method[1] == 3:#whisper-japanese
                    self.whisper_exe(language="ja", file_path = self.audio_path)
                if self.stt_method[1] == 4:#whisper-chinese
                    self.whisper_exe(language="zh", file_path = self.audio_path)
        
    def convert_video_to_audio_ffmpeg(self, video_path, output_ext="mp3"):#wav가 좋은지, mp3를 써도 상관없는지 써봐야 알 듯.
        
        self.save_audio = video_path + "." + output_ext
        print(self.save_audio)
        print(video_path)
        # ext = Path(video_path).stem
        self.my_clip = mp.VideoFileClip(video_path)
        self.my_clip.audio.write_audiofile(self.save_audio)
        
        return self.save_audio

    #위스퍼 모델 실행
    def whisper_exe(self, language, file_path):#language = None이면 위스퍼가 auto로 진행됨.
        
        if torch.cuda.is_available():#cpu, gpu 확인해서 진행.
            print("사용할 수 있는 gpu가 있습니다. \nnvidia gpu로 진행합니다.")
            self.device = "cuda"
        else:
            print("사용할 수 있는 gpu가 감지되지 않습니다. cpu로 진행합니다.")
            self.device = "cpu"

        self.language = language
        model_path = snapshot_download(repo_id= "gemble/whisper-large-v2-ct2-int8_float16" , library_name= "whisper-large-v2-ct2-int8_float16", cache_dir="VoatG/model" )
        print(model_path)
        model_path = model_path + "\whisper-large-v2-ct2-int8_float16"
        self.model = WhisperModel(model_path= model_path, device=self.device, compute_type="int8_float16")
        self.audio_file_path = file_path

        self.segments, self.info = self.model.transcribe(self.audio_file_path, language=self.language)
        if self.video_right == 1:#작업 끝난 오디오 삭제.
            send2trash.send2trash(self.audio_file_path)
            self.video_right = 0

        self.segmentId = 0
        nn = Path(file_path).with_suffix('.srt')
        #음성 분석해서 나온 자막 저장.
        with open(nn, "w", encoding="utf-8") as save:
            for self.segment in self.segments:
                self.startTime = "0" + str(Timedelta(seconds=int(self.segment.start))) + ",000"
                self.endTime = "0" + str(Timedelta(seconds=int(self.segment.end))) + ",000"
                
                self.segmentId += 1
                if self.segment.text[0] == " ":
                    self.script = self.segment.text[1:]
                else:
                    self.script = self.segment.text
                self.segment = f"{self.segmentId}\n{self.startTime} --> {self.endTime}\n{self.script}\n\n"
                print(self.segment)
                save.write(self.segment)
        
        print("완료")




if __name__ == "__main__":
    
    print("volt")

    #video_path = sys.argv[1]
    #a = recognizion(video_path)