import os
import sys
import urllib.request


# papago api
class Trans_api:
    def __init__(self, setting):
        self.papago_free_client_id = setting["api_keys"]["papago_free_api"]  # 개발자센터에서 발급받은 Client ID 값
        self.papago_free_client_secret = setting["api_keys"]["papago_free_api"]  # 개발자센터에서 발급받은 Client Secret 값
        self.source_lang = setting["source_lang"]
        self.target_lang = setting["target_lang"]

    def papago_free_api(self):
        encText = urllib.parse.quote("반갑습니다")
        data = f"source={self.source_lang}&target={self.target_lang}&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.papago_free_client_id)
        request.add_header("X-Naver-Client-Secret", self.papago_free_client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            print(response_body.decode("utf-8"))
        else:
            print("Error Code:" + rescode)


# todo
# 파일 번역할 때, 특정 문자가 들어가있으면 그 줄은 번역하지 않도록 하는 설정.
