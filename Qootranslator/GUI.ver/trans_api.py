import os
import sys
import urllib.request


# papago api
class Trans_api:
    def __init__(self, setting):
        self.papago_free_client_id = setting["api_keys"]["papago_free_api"]  # 개발자센터에서 발급받은 Client ID 값
        self.papago_free_client_secret = setting["api_keys"]["papago_free_api"]  # 개발자센터에서 발급받은 Client Secret 값

    def papago_free_api(self):
        client_id = "YOUR_CLIENT_ID"  # 개발자센터에서 발급받은 Client ID 값
        client_secret = "YOUR_CLIENT_SECRET"  # 개발자센터에서 발급받은 Client Secret 값
        encText = urllib.parse.quote("반갑습니다")
        data = "source=ko&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.papago_free_client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            print(response_body.decode("utf-8"))
        else:
            print("Error Code:" + rescode)
