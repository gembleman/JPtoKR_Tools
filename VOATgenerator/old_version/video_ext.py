import moviepy.editor as mp
from pathlib import Path
import sys

from faster_whisper import WhisperModel
import torch
import psutil
from timedelta import Timedelta

import librosa

class recognizion:
    def __init__(self, file_dics, method):
        self.stt_method = method
        self.file_dics = file_dics
        print(file_dics)
        print(method)
        
        

    def run(self):
        #self.aaa = self.file_dics.keys
        for self.file_path in self.file_dics.keys():
            
            if self.file_dics[self.file_path] == "video+sub":
                print(f"{self.file_path} 비디오와 자막 인식했습니다.")
                #비디오 파일을 넣으면 자동으로 같은 이름의 자막 파일 넣기.
                self.audio_path = self.convert_video_to_audio_ffmpeg(self.file_path)
                self.nym = "sub"#자막 파일을 이용해서 인식해라.
            
            if self.file_dics[self.file_path] == "video_only":
                print(f"{self.file_path} 비디오 인식했습니다.")
                self.audio_path = self.convert_video_to_audio_ffmpeg(self.file_path)
                self.nym = "vad"

            if self.file_dics[self.file_path] == "audio":
                print(f"{self.file_path} 오디오 포맷입니다.")
                self.nym = "vad"#바드를 써라 - 폐기. - 바드가 위스퍼보다 "음성 구간 탐지 기능"이 정확하지 않음.

            #whisper 모델 택했다면 이쪽으로
            if self.stt_method[0] == 1:#whisper-
                if self.stt_method[1] == 0 or self.stt_method[1] == 1:#whisper-auto
                    self.whisper_exe(language=None, file_path = self.audio_path)
                if self.stt_method[1] == 2:#whisper-korean
                    self.whisper_exe(language="ko", file_path = self.audio_path)
                if self.stt_method[1] == 3:#whisper-english
                    self.whisper_exe(language="en", file_path = self.audio_path)
                if self.stt_method[1] == 4:#whisper-japanese
                    self.whisper_exe(language="ja", file_path = self.audio_path)
                if self.stt_method[1] == 5:#whisper-chinese
                    self.whisper_exe(language="zh", file_path = self.audio_path)
        
    def Vad_use(self):
        '''
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',model='silero_vad',)
        (get_speech_timestamps,_, read_audio,*_) = utils

        sampling_rate = 16000 # also accepts 8000
        wav = read_audio('en_example.wav', sampling_rate=sampling_rate)
        # get speech timestamps from full audio file
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=sampling_rate)
        fueo = []
        
        for timestamp in speech_timestamps:
            #밀리세컨드, 초로 변환.
            fueo.append([timestamp['start'] / sampling_rate, timestamp['end'] / sampling_rate])
        
        
        
        #self.time_intervals = [[54, 60], [19, 27], [40.600, 53.120]]
    
        
        Splits the audio_array according to the time_intervals
        and returns a audio_segments list with multiple audio_arrays
        together with the time_intervals passed to the function

        

        # sort the audio segments by start time
        self.time_intervals = sorted(fueo, key=lambda x:x[0])

        # reset the audio segments list
        self.audio_segments = []
        
        self.sr = 16_000
        # if there are time segments
        if self.time_intervals is not None and self.time_intervals and len(self.time_intervals) > 0:

            # take each time segment
            for time_interval in self.time_intervals:

                # calculate duration based on start and end times!!

                # and add it to an audio segments list
                # the format is [start_time, end_time, audio_array]
                audio_segment = [time_interval[0], time_interval[1],self.audio_array[int(time_interval[0] * self.sr): int(time_interval[1] * self.sr)]]

                self.audio_segments.append(audio_segment)


        # if time_intervals is empty, define it as a single segment, 
        # from the beginning to the end (i.e. we're transcribing the full audio)
        else:
            self.time_intervals = [[0, len(self.audio_array)/self.sr]]
            self.audio_segments = [0, len(self.audio_array/self.sr), self.audio_array]
        '''


    def convert_video_to_audio_ffmpeg(self, video_path, output_ext="mp3"):
        
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
        model_path = r"C:\Users\nsoop\Desktop\whisper-large-v2-ct2-int8_float16"
        self.model = WhisperModel(model_path= model_path, device=self.device, compute_type="int8_float16")
        self.audio_file_path = file_path
        
        # load audio file using librosa and get the audio_array
        #self.audio_array, self.sr = librosa.load(self.audio_file_path, sr=16_000)
        #self.Vad_use()
        #print(f'Selected intervals for transcription:\n {self.time_intervals} \n')

        # call split function

        #print(f'time intervals:\n {self.time_intervals} \n')
        #print(f'audio segments:\n {self.audio_segments} \n')

        #self.transcribe_segments(self.audio_segments)
        '''
        Transcribes only the passed audio segments 
        and offsets the transcription segments start and end times

        '''
        '''
        with open("text.srt", "w", encoding="utf-8") as save:
            # transcribe each audio segment
            for i, audio_segment in enumerate(self.audio_segments):

                print("Segment {} - second {} to {}".format(i, audio_segment[0], audio_segment[1]))

                # run whisper transcribe on the audio segment
                self.segment, self.info = self.model.transcribe(audio_segment[2], language=self.language)

                startTime = "0" + str(Timedelta(seconds=int(audio_segment[0]))) + ",000"
                endTime = "0" + str(Timedelta(seconds=int(audio_segment[1]))) + ",000"
                self.text = next(self.segment).text
                
                
                segmentId = i + 1
                print(self.text)
                if self.text[0] == " ":
                    script = self.text[1:]
                else:
                    script = self.text
                segment = f"{segmentId}\n{startTime} --> {endTime}\n{script}\n\n"
                save.write(segment)

                #음성 분석해서 나온 자막 저장.
        '''

        #self.segment, self.info = self.model.transcribe(audio_segment[2], language=self.language)
        self.segments, self.info = self.model.transcribe(self.audio_file_path, language=self.language)
        self.segmentId = 0
        #음성 분석해서 나온 자막 저장.
        with open("text.srt", "w", encoding="utf-8") as save:
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