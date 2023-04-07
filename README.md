# 답답해서 만든 도구들
허접한 코드지만, 일단 돌아가긴 돌아간다. 

## VOATgenerator는 뭔가 
원래는 제가 쓰려고 만들다가  
"사용자가 무료, 무제한으로 이용할 수 있는 음성 인식 자막 생성 프로그램(비디오 지원)"  
이런 거창한 목적을 갖다 붙이고 배포합니다.  

클로바 노트나, Vrew라는 프로그램이 비슷한 기능으로, 무료로 쓸 수 있는데요.  
그렇지만, 언젠가 돈을 내고 써야하는 날이 오죠.  

반면, 이 프로그램은 완전 무료입니다. 음성 인식도 나름 괜찮아요.  
또, 보안상의 이유나 기타 이유로 온라인으로 업로드하기 힘든 오디오 파일도  
이 프로그램을 쓰면, 로컬 컴퓨터에서 해결할 수 있다는 것도 장점입니다.  

지원하는 언어는, 영어, 한국어, 일본어, 중국어, 등이 있습니다.  
언어 선택은 기본이 자동인데,  
일본어면 일본어, 영어면 영어로 지정해주면 좋습니다. 별로 차이는 없는데 약간 빨라집니다.  
윗 네 언어 말고 다른 언어면 자동 인식으로 두세요.  

### 기능
비디오나 오디오 파일 이름과 같은 이름으로 된 SRT 자막 파일이 있다면 VOAT가 인식합니다.  
그럼 VOAT가 자막 타이밍에 맞춰 오디오를 잘라내고  
거기에서 인식한 음성 텍스트를 자막 파일에 집어넣습니다.  

### 설치 방법
1.압축파일 다운 받고 압축풀기..  
ffmpeg라는 프로그램이 설치되어 있지 않으면, 따로 설치하거나, 아니면 같이 배포한 배치파일을 실행할 것.  
2.돗단배 아이콘을 단 VOATgenerator.exe 클릭.  
3.비디오나 오디오 파일들 드래그 앤 드롭.  
4.인식할 언어 설정하고, 음성 인식 시작 버튼 누르기.  
5.침착하게 프롬프트창을 보며 기다리기.(오디오가 길수록, 그래픽카드가 별로일수록 느립니다.)  

### 필수사양
돌리는 데 필요한 컴퓨터 사양은 먼저 엔비디아 그래픽 카드여야 하고 vram이 최소 4기가는 되야 합니다.  
엔비디아 그래픽카드가 없을 경우, 자동으로 cpu로 진행되는데 그럼 매우 느립니다.  
램은 최소 8기가, cpu는 적당한 거.  
저장 용량은 6.64기가 정도 필요합니다. 최대한 줄여서 저 정도네요. 게임 하나 받는다고 생각하셔요...  

### 기타 정보
프로그램이 사용하는 음성 인식 모델은 openai 회사에서 배포한 whisper large-v2 모델에서  
약간 개조를 거친 faster-whisper large-v2모델을 사용합니다.  

음성 인식이 가장 정확하게 되는 언어는 스페인어 1위, 영어 3위, 일본어 6위, 한국어 27위, 중국어 30위 순입니다.  
도표 참조하세요  
[https://github.com/openai/whisper](https://github.com/openai/whisper)  

VOice Analyzing Text라서 VOAT입니다. 완전 어거지인데..  

### used library
[https://github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper)  
[https://github.com/librosa/librosa](https://github.com/librosa/librosa)  
[https://github.com/cdown/srt](https://github.com/cdown/srt)  





## ezTransWeb_fix는 뭔가
Source by [https://github.com/HelloKS/ezTransWeb](https://github.com/HelloKS/ezTransWeb)  
원래 있던 코드에서  
파이썬 3.11 32비트환경에서 Translator++ 지원이 가능하도록 몇몇 부분을 수정.  
기존에는 코드만 있었지만 사용하기 편하도록 exe파일로 만들었다. Release로 가서 받자.  
[다운로드 링크](https://github.com/gembleman/JPtoKR_Tools/releases/tag/eztransWeb)  

trans.eztransweb.js는 Translator++에 이지트랜스 지원을 위한 플러그인.  
Source by [https://arca.live/b/simya/57025402](https://arca.live/b/simya/57025402)  
batchDelay를 1에서 0.1로 바꾼 것 빼고는 수정한 부분은 없다.  
적용 방법은  
Translator++\www\js\autoload  
경로로 들어가 이 파일을 집어넣으면 된다.  
