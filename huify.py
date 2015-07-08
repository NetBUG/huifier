#coding=utf-8
from bs4 import BeautifulSoup
import html2text
import requests
from topia.termextract import extract
from topia.termextract import tag

tagger = tag.Tagger('english')
tagger.initialize()
 
 # create the extractor with the tagger
extractor = extract.TermExtractor(tagger=tagger)
extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=3)
url = "http://habrahabr.ru"
doc = requests.get(url).content
doc = BeautifulSoup(doc,from_encoding="utf-8")
[s.extract() for s in doc(u'script')]
[s.extract() for s in doc(u'style')]
doc = doc.get_text()
#doc = html2text.html2text(doc)
kw = extractor(doc)

''' test: huify(u'эту неделю').encode('utf-8') == u'эту xyеделю' '''
def huify(expr):
    word = expr
    if expr.rfind(' ') > -1:
        word = expr[expr.rindex(' ')+1:]
    vowels = set(u'aeiouyаеиоуыяюё')
    mz = len(word)
    for vowel in vowels:
        if word.find(vowel) >= 0:
            mz = min(word.find(vowel), mz)
    if mz == len(word):
        return expr
    #+ TODO: йотирование «ю»: лучший-хуючший
    oldword = word
    if oldword[mz] == u'у':
        word = word[:mz] + u'ю' + word[mz + 1:]
    if oldword[mz] == u'о':
        word = word[:mz] + u'ё' + word[mz + 1:]
    if oldword[mz] == u'а':
        word = word[:mz] + u'я' + word[mz + 1:]
    return expr.replace(oldword, oldword+'-xy'+word[mz:])

kws = []
for word in kw:
    print word[0].encode('utf-8')
    #doc = doc.replace(word[0], huify(word[0]))
    kws.append(word[0])

doc = doc.split('\n')
for ln, line in enumerate(doc):
    nl = ''
    for word in line.split(' '):
        if word in kws and len(word) > 3:
            nl += huify(word)
        else:
            nl += word
        nl += ' '
    doc[ln] = nl

fh = open('out.txt', 'w')
fh.write('\n'.join(doc).encode('utf-8'))
fh.close()