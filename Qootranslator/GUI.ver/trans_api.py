import os
import sys
import urllib.request
import deepl
import six
from google.cloud import translate_v2
import logging
from concurrent.futures import ThreadPoolExecutor

def init_logger():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(threadName)s] %(message)s"))
    logger = logging.getLogger("record")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# papago api
class Trans_api:
    def __init__(self, setting):
        self.papago_free_keys = setting["api_keys"]["papago_free_api"]
        self.papago_paid_keys = setting["api_keys"]["papago_paid_api"]
        self.papago_free_index = 0
        self.papago_paid_index = 0
        self.papago_dic = {"한국어":"ko","영어":"en","일본어":"ja","중국어 간체":"zh-CN","중국어 번체":"zh-TW","베트남어":"vi","인도네시아어":"id","태국어":"th", "독일어":"de", "러시아어":"ru", "스페인어":"es", "이탈리아어":"it", "프랑스어":"fr"}
        #"일본어", "한국어", "영어", "중국어 간체", "중국어 번체", "베트남어", "인도네시아어", "태국어", "독일어", "러시아어", "스페인어", "이탈리아어", "프랑스어"
        
        self.deepL_api_keys = setting["api_keys"]["deepL_api"]
        self.deepL_dic = {"한국어":"KO", "일본어":"JA", "영어":"EN", "중국어":"ZH", "불가리아어":"BG", "체코어":"CS","덴마크어":"DA","독일어":"DE","그리스어":"EL","스페인어":"ES","에스토니아어":"ET","핀란드어":"FI","프랑스어":"FR","헝가리어":"HU",
                          "인도네시아어":"ID","이탈리아어":"IT","리투아니아어":"LT","라트비아어":"LV","노르웨이어":"NB","네덜란드어":"NL","폴란드어":"PL","포르투갈어":"PT","루마니아어":"RO","러시아어":"RU","슬로바키아어":"SK",
                          "슬로베니아어":"SL","스웨덴어":"SV","터키어":"TR","우크라이나어":"UK"}
        #["한국어", "일본어", "영어", "중국어", "불가리아어", "체코어","덴마크어","독일어","그리스어","스페인어","에스토니아어","핀란드어","프랑스어","헝가리어",
        #"인도네시아어","이탈리아어","리투아니아어","라트비아어","노르웨이어","네덜란드어","폴란드어","포르투갈어","루마니아어","러시아어","슬로바키아어",
        #"슬로베니아어","스웨덴어","터키어","우크라이나어"]

        self.google_keys = setting["api_keys"]["google_api"]
        self.google_dic = {"한국어":"ko","일본어":"ja","영어":"en","중국어 간체":"zh-CN", "중국어 번체":"zh-TW","포르투갈어":"pt", "스페인어":"es", "프랑스어":"fr", "독일어":"de", "베트남어":"vi", "튀르키예어":"tr",
                             "아프리칸스어":"af","알바니아어":"sq","암하라어":"am","아랍어":"ar","아르메니아어":"hy","아제르바이잔어":"az","밤바라어":"bm","바스크어":"eu","벨라루스어":"be",
                             "벵골어":"bn","보지푸리어":"bho","불가리아어":"bg","카탈루냐어":"ca","세부아노어":"ceb", "코르시카어":"co","크로아티아어":"hr","체코어":"cs","덴마크어":"da","디베히어":"dv","도그리어","네덜란드어","에스페란토어",
                             "에스토니아어":"et","에웨어":"ee","필리핀어":"fil","프리지아어":"fy","갈리시아어":"gl","조지아어":"ka","그리스어":"el","과라니아어":"gn","구자라트어":"gu","아이티크리올어":"ht","하우사어":"ha","하와이어":"haw","히브리어":"he",
                             "힌디어":"hi","몽어":"hmn","헝가리어":"hu","아이슬란드어":"is","이보어":"ig","일로카노어":"ilo","인도네시아어":"id","아일랜드어":"ga","자바어":"jv","칸나디어":"kn","카자흐어":"kk","크메르어":"km","키냐르완다어":"rw","콘칸어":"gom","크리오어":"kri",
                             "쿠르드어":"ku","소라니어":"ckb","키르기스어":"ky","라오어":"lo","라틴어":"la","라트비아어":"lv","링갈라어":"ln","리투아니아어":"lt","루간다어":"lg","룩셈베르크어":"lb","마케도니아어":"mk","마이틸리어":"mai","말라가시어":"mg","말레이어":"ms",
                             "말라얄람어":"ml","몰타어":"mt","마오리어":"mi","마라티어":"mr","메이테이어":"mni-Mtei","미조어":"lus","몽골어":"mn","미얀마어":"my","네팔어":"ne","노르웨이어":"no","니안자어":"ny","오리야어":"or","오로모어":"om","파슈토어":"ps","페르시아어":"fa",
                             "폴란드어":"pl","펀자브어":"pa","케추아어":"qu","루마니아어":"ro","러시아어":"ru","사모아어":"sm","산스크리트어":"sa","게일어":"gd","북소토어":"nso","세르비아어":"sr","세소토어":"st","쇼나어":"sn","신디어":"sd",
                             "스리랑카어":"si","슬로바키아어":"sk","슬로베니아어":"sl","소말리어":"so","순다어":"su","스와힐리어":"sw","스웨덴어":"sv","필리핀어":"tl","타지크어":"tg","타밀어":"ta","타타르어":"tt","텔루구어":"te","태국어":"th","티그리냐어":"ti",
                             "총가어":"ts","투르크멘어":"tk","트위어":"ak","우크라이나어":"uk","우르두어":"ur","위구르어":"ug","우즈베크어":"uz","웨일즈어":"cy","코사어":"xh","이디시어":"yi","요루바어":"yo","줄루어":"zu"}

        self.source_lang = setting["source_lang"]
        self.target_lang = setting["target_lang"]
        self.log = init_logger()
        

    def papago_api(self, source_txt):#클립보드 번역용
        
        papago_keys = self.papago_free_keys.keys()

        encText = urllib.parse.quote(source_txt)
        data = f"source={self.papago_dic[self.source_lang]}&target={self.papago_dic[self.target_lang]}&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", papago_keys[n])
        request.add_header("X-Naver-Client-Secret", self.papago_free_keys[papago_keys[n]])
        try:
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        except Exception as e:
            print(e)
            if "HTTP Error 429" in str(e):
                self.papago_index += 1
            return 429
        rescode = response.getcode()
        translated_text = ""
        if rescode == 200:
            response_body = response.read()
            translated_text = response_body.decode("utf-8")
            print(translated_text)
        else:
            print("Error Code:" + rescode)
            if rescode == "api키 변경":
                return 429
        return translated_text

    # todo
    # 파일 번역할 때, 특정 문자가 들어가있으면 그 줄은 번역하지 않도록 하는 설정.
    #소스 언어 자동 감지 추가.

    def deepL_api(self):
        #한 줄 번역인지, 문서번역인지 나누기.
        deepL_translator = deepl.Translator(self.deepL_api_key)
        if self.source_lang == "자동감지":
            result = deepL_translator.translate_text(self.source_text,target_lang=self.deepL_dic[self.target_lang])
        else: 
            result = deepL_translator.translate_text(self.source_text,source_lang=self.deepL_dic[self.source_lang],target_lang=self.deepL_dic[self.target_lang])
        
        return result.text#번역된 텍스트

    def google_api(self):
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        translate_client = translate_v2.Client()
        result = {}
        if self.source_lang == "자동감지":
            result = translate_client.translate(text,target_language=self.google_dic[self.target_lang])
        else:
            result = translate_client.translate(text, source_language=self.google_dic[self.source_lang],target_language=self.google_dic[self.target_lang])

        print(f"Text: {result["input"]}")
        print(f"Translation: {result["translatedText"]}")
        print(f"Detected source language: {result["detectedSourceLanguage"]}")

        return result["translatedText"]
    
    def trans_file(self,trans_engine,file_path):#파일 번역용    
        self.log.info("파일 번역 시작")
        engine_dic = {"papago":self.papago_api,"deepL":self.deepL_api,"google":self.google_api}
        
        with open(file_path, "r", encoding="utf-8") as f:
            source_texts = f.readlines()

        with ThreadPoolExecutor(max_workers=None, thread_name_prefix="thread") as executor:
            results = executor.map(engine_dic[trans_engine], source_texts)
        self.log.info("파일 번역 종료")
        
        with open(file_path / "번역완료.txt", "w", encoding="utf-8") as f:
            f.writelines(results)
        #utf-8-sig나 기타 인코딩은 경고문 출력하기.

if __name__ == "__main__":
    #파파고 api 테스트
    # papago = Translator("ko","en","안녕하세요")
    # papago.papago_api()
    # papago.papago_repeat()

    #딥엘 api 테스트
    # deepL = Translator("ko","en","안녕하세요")
    # deepL.deepL_api()

    #구글 api 테스트
    # google = Translator("ko","en","안녕하세요")
    # google.google_api()
    pass