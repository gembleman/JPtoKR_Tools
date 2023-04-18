import ctranslate2
import transformers
import os
import pyperclip
import re
#nllb is facebook nllb-200-distilled-600M_int8_float16 model.

print(os.getcwd())
src_lang = "jpn_Jpan"
tgt_lang = "kor_Hang"

translator = ctranslate2.Translator(r'I:\nllb-3.3b_int8_float16',device = 'cuda')
tokenizer = transformers.AutoTokenizer.from_pretrained("facebook/nllb-200-3.3B", src_lang=src_lang)
#text = '스타푸르트はどうですか？'

while True:
    text = pyperclip.waitForNewPaste()
    text = re.sub('[（）]','',text)
    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(text))
    target_prefix = [tgt_lang]
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    target = results[0].hypotheses[0][1:]

    print(tokenizer.decode(tokenizer.convert_tokens_to_ids(target)))


#애기 모델도 만들 생각.