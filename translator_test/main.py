from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

source = 'jpn_Jpan' # English
target = 'kor_Hang' # Korean
translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target, device=0)

text = 'スターフルーツはどうですか？'

output = translator(text, max_length=400)

translated_text = output[0]['translation_text']

print(translated_text) # '안녕하세요, 반가워요'
