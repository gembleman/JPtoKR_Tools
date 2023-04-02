import ffmpeg
import faster_whisper
import torch
import send2trash
import huggingface_hub
import librosa
import srt
import pathlib
import datetime

class recognizion:
    def __init__(self, file_dics, method):
        self.stt_method = method
        self.file_dics = file_dics
        #print(file_dics)
        #print(method)
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
                self.file_path_sub = pathlib.Path(self.file_path).with_suffix('.srt')
                self.load_sub(str(self.file_path_sub))

            if self.file_dics[self.file_path] == "video_only":
                print(f"{self.file_path} 비디오 인식했습니다.")
                self.audio_path = self.convert_video_to_audio_ffmpeg(self.file_path)
                self.nym = "None"
                self.video_right = 1
            
            if self.file_dics[self.file_path] == "audio+sub":
                print(f"{self.file_path} 오디오와 자막 인식했습니다.")
                #오디오 파일을 넣으면 자동으로 같은 이름의 자막 파일 넣기.
                self.audio_path = self.file_path
                self.nym = "sub"#자막 파일을 이용해서 인식해라.
                self.file_path_sub = pathlib.Path(self.file_path).with_suffix('.srt')
                self.load_sub(str(self.file_path_sub))
            
            if self.file_dics[self.file_path] == "audio_only":
                print(f"{self.file_path} 오디오 인식했습니다.")
                self.audio_path = self.file_path
                self.nym = "None"

            if self.audio_path == 1:
                print("오류, 프로세스 종료")
                return 1

            #whisper 모델 택했다면 이쪽으로
            if self.stt_method[0] == 0:#whisper-
                if self.stt_method[1] == 0:#whisper-auto
                    self.whisper_exe(language=None, file_path = self.audio_path)
                if self.stt_method[1] == 1:#whisper-korean
                    self.whisper_exe(language="ko", file_path = self.audio_path)
                if self.stt_method[1] == 2:#whisper-english
                    self.whisper_exe(language="en", file_path = self.audio_path)
                if self.stt_method[1] == 3:#whisper-japanese
                    self.whisper_exe(language="ja", file_path = self.audio_path)
                if self.stt_method[1] == 4:#whisper-chinese
                    self.whisper_exe(language="zh", file_path = self.audio_path)
    

    def load_sub(self, sub_path):#자막 파일 로드.
        self.sub_path = sub_path
        with open(self.sub_path,'r',encoding = 'utf-8') as f:
            self.time_intervals = []
            for sub in list(srt.parse(f)):
                self.time_intervals.append([sub.start.total_seconds(), sub.end.total_seconds()])
                #자막 타이밍에 밀리세컨드까지 통째로 모델에 넣었더니, 오류남. 타이밍에서 세컨드까지만 인식됨. 그래서 세컨드까지만 자름.
                #12:52.255면 .255를 자르고 12:52만 남겼다는 얘기. 
        
        self.audio_array, sr = librosa.load(self.audio_path, sr=16000)
        '''
        time_intervals에 따라 audio_array를 분할하고 함수에 전달된 time_intervals와 함께 여러 audio_array가 포함된 audio_segments 목록을 반환합니다.
        '''
        # sort the audio segments by start time
        self.time_intervals = sorted(self.time_intervals, key=lambda x:x[0])

        # reset the audio segments list
        self.audio_segments = []

        # if there are time segments
        if self.time_intervals is not None:

            # take each time segment
            for self.time_interval in self.time_intervals:
                # calculate duration based on start and end times!!
                # and add it to an audio segments list
                # the format is [start_time, end_time, audio_array]
                self.audio_segment = [self.time_interval[0], self.time_interval[1], self.audio_array[int(self.time_interval[0] * sr):  int(self.time_interval[1] * sr)]]

                self.audio_segments.append(self.audio_segment)


        # if time_intervals is empty, define it as a single segment, 
        # from the beginning to the end (i.e. we're transcribing the full audio)
        else:
            self.time_intervals = [[0, len(self.audio_array)/sr]]
            self.audio_segments = [0, len(self.audio_array/sr), self.audio_array]

        return self.audio_segments
    
    def convert_video_to_audio_ffmpeg(self, video_path,):#wav가 좋은지, mp3를 써도 상관없는지 써봐야 알 듯. - 작업 영상의 오디오를 그대로 복사하기로 함. 해결.
        self.video_path = video_path
        print(self.video_path)
        try:
            codec_name = ffmpeg.probe(self.video_path)['streams'][1]['codec_name']#오디오 코덱 값 찾으려고.
        except Exception as inst:
            print(inst)
            print("아마도 비디오 파일에 오디오가 없습니다.")
            return 1
        self.audio_path2 = pathlib.Path(video_path).with_suffix('.'+codec_name)
        ffmpeg.input(self.video_path, vn=None).output(str(self.audio_path2), acodec="copy").run()#ffmpeg가 설치되어 있어야 함. 하여튼 이 줄로 오디오 뽑아냄.

        return str(self.audio_path2)

    #위스퍼 모델 실행
    def whisper_exe(self, language, file_path):#language = None이면 위스퍼가 auto로 진행됨.
        
        if torch.cuda.is_available():#cpu, gpu 확인해서 진행.
            print("사용할 수 있는 gpu가 있습니다. \nnvidia gpu로 진행합니다.")
            self.device = "cuda"
            self.compute_type = "int8_float16"
        else:
            print("사용할 수 있는 gpu가 감지되지 않습니다. cpu로 진행합니다.")
            self.device = "cpu"
            self.compute_type = "int8"

        self.language = language
        self.audio_file_path = file_path
        model_path = huggingface_hub.snapshot_download(repo_id= "gemble/whisper-large-v2-ct2-int8_float16" , library_name= "whisper-large-v2-ct2-int8_float16", cache_dir="VoatG/model")#model 다운로드
        #print(model_path)
        model_path = model_path + "\whisper-large-v2-ct2-int8_float16"
        self.model = faster_whisper.WhisperModel(model_path, device = self.device, compute_type=self.compute_type)
        if self.nym == "sub":
            with open(self.file_path_sub, "w", encoding="utf-8") as save:
                for i, audio_segment in enumerate(self.audio_segments):
                    self.i2 = i+1
                    print(f"Segment {self.i2} - second {audio_segment[0]} to {audio_segment[1]}")

                    # run whisper transcribe on the audio segment
                    #result = model.transcribe(audio_segment[2],task=task, verbose=False,)
                    self.segments, self.info = self.model.transcribe(audio_segment[2],language=self.language)
                    self.startTime = "0" + str(datetime.timedelta(seconds=audio_segment[0])) + ",000"
                    
                    self.endTime = "0" + str(datetime.timedelta(seconds=audio_segment[1])) + ",000"
                    self.script = ""
                    for self.segment in self.segments:
                        if self.segment.text[0] == " ":
                            self.script = self.script + self.segment.text[1:]
                        else:
                            self.script = self.script + self.segment.text
                    self.segment = f"{self.i2}\n{self.startTime} --> {self.endTime}\n{self.script}\n\n"
                    print(self.segment)
                    save.write(self.segment)

        if self.nym == "None":
            self.segments, self.info = self.model.transcribe(self.audio_file_path, language=self.language)
            
            nn = pathlib.Path(file_path).with_suffix('.srt')
            #음성 분석해서 나온 자막 저장.
            with open(nn, "w", encoding="utf-8") as save:
                for self.segmentId, self.segment in enumerate(self.segments):
                    self.startTime = "0" + str(datetime.timedelta(seconds=self.segment.start)) + ",000"
                    self.endTime = "0" + str(datetime.timedelta(seconds=self.segment.end)) + ",000"
                    
                    if self.segment.text[0] == " ":
                        self.script = self.segment.text[1:]
                    else:
                        self.script = self.segment.text
                    self.segment = f"{self.segmentId + 1}\n{self.startTime} --> {self.endTime}\n{self.script}\n\n"
                    print(self.segment)
                    save.write(self.segment)

        if self.video_right == 1:#작업 끝난 오디오 삭제.
            send2trash.send2trash(self.audio_file_path)
            self.video_right = 0
        
        print("완료")

#todo - liblosa를 이용해 오디오 타임스탬프가 있는 자막을 이용해 음성 구간을 추출해서 텍스트 추출하는 기능 만들 것.



if __name__ == "__main__":
    
    print("volt")

    #video_path = sys.argv[1]
    #a = recognizion(video_path)
    #a.convert_video_to_audio_ffmpeg(video_path="")


    #ffmpeg로 가려고 생각 중.