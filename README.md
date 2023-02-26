# 답답해서 만든 도구들
허접한 코드지만, 일단 돌아가긴 돌아간다. 


## ezTransWeb_fix는 뭔가
Source by https://github.com/HelloKS/ezTransWeb
원래 있던 코드에서  
파이썬 3.11 32비트환경에서 Translator++ 지원이 가능하도록 몇몇 부분을 수정.
원래는 코드만 있었지만 사용하기 편하도록 exe파일로 만들었다. Release로 가서 받자.
  
trans.eztransweb.js는 Translator++에 이지트랜스 지원을 위한 플러그인.  
Source by https://arca.live/b/simya/57025402  
batchDelay를 1에서 0.1로 바꾼 것 빼고는 수정한 부분은 없다.  
적용 방법은  
Translator++\www\js\autoload  
경로로 들어가 이 파일을 집어넣으면 된다.  
