import re

text = "작은 새에게는 나쁘지만, 텐에지(天枝) 씨와 비교하면 아무래도 아이로 보인다."
text = text.replace("작은 새","코토리")
print(text)
quit()



text = "「天枝さん。ムカついてたら殴っていいよ？　グーで」「だからマブだって言ってんじゃん！！　しかもグーでとか手加減なしじゃん！！！」「あはは……大丈夫ですよ。みんなからそう呼ばれてますから」小鳥の悪ふざけかとも思ったが、どうやら違うらしい。「ごめん小鳥。疑って悪かったよ」"
a = []
def find_all(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

text = text.split('　')
for t1 in text:
    txt_mini = re.sub('[「」？！　]',t1)
    #번역하고.

'''
    find1 = list(find_all("「",t1))
    find2 = list(find_all("」",t1))
    find3 = list(find_all("？",t1))
    find4 = list(find_all("！",t1))
    find5 = list(find_all("　",t1))
'''



'''
#그냥 해본 거
text = "「天枝さん。ムカついてたら殴っていいよ？　グーで」"
a = []
def find_all(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

text = text.split('　')
for t1 in text:
    #txt_mini = re.sub('[「」　]','',t1)
    #quit()
    source = tokenizer.convert_ids_to_tokens(tokenizer.encode(t1))
    target_prefix = [tgt_lang]
    results = translator.translate_batch([source], target_prefix=[target_prefix])
    target = results[0].hypotheses[0][1:]

    print(tokenizer.decode(tokenizer.convert_tokens_to_ids(target)))
'''