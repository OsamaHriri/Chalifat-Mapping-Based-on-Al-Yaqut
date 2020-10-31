import arramooz.arabicdictionary
import  arramooz.stopwordsdictionaryclass
from farasa.stemmer import FarasaStemmer
import pandas as pd
import re
import time
from collections import Counter
from  stop_words_handler import Stopwords_Handler
mydict = arramooz.stopwordsdictionaryclass.StopWordsDictionary('classedstopwords')
wordlist = [u'وبين ','وبيهما ']
# tmp_list = []
# for word in wordlist:
#     foundlist = mydict.lookup(word)
#     for word_tuple in foundlist:
#         word_tuple = dict(word_tuple)
#         vocalized = word_tuple['vocalized']
#         tmp_list.append(dict(word_tuple))
# print(tmp_list)
sample =\
''' 
يُشار إلى أن اللغة العربية  بين تحت فوق يتحدثها أكثر من 422 مليون نسمة ويتوزع متحدثوها
 في المنطقة المعروفة باسم الوطن العربي بالإضافة إلى العديد من المناطق ال
أخرى المجاورة مثل الأهواز وتركيا وتشاد والسنغال وإريتريا وغيرها.وهي اللغ
ة الرابعة من لغات منظمة الأمم المتحدة الرسمية الست. 
'''
s = Stopwords_Handler()
stemmer = FarasaStemmer(interactive=True)
# stemmed_text = stemmer.stem('وبينهما')
# print(stemmed_text)
# tmp_list = []
# word_tuple = mydict.lookup(stemmed_text)[0]
#
# word_tuple = dict(word_tuple)
# vocalized = word_tuple['vocalized']
# tmp_list.append(dict(word_tuple))
# print(tmp_list[0]['word_class'])

"""create vocab or preps"""

def clean_text(w):
    tick = time.time()

    punc =  '''#`÷×؛<>_()*&^%][ـ/"؟'{}~¦+|!”…“–ـ'''

    # Cleaning the html elements
    clean = re.compile(r'<.*?>')
    w = clean.sub('', w)

    # Removing the punctuations
    for ch in punc:
        w = w.replace(ch, '')

    # Cleaning the urls

    w = re.sub(r'https?://\S+|www\.\S+', '', w)
    # Cleaning Numbers
    w = re.sub(r'\d+', '', w)

    w = w.replace('Milestone','')
    w = w.replace('PageVP', '')
    tack = time.time()

    return w

def retrun_prers(text):
    tick = time.time()
    tmp_list = []
    words=[]
    #Takes about 2.2 sec
    tolkens = stemmer.stem(text)
    tack = time.time()

    for word in tolkens.split(' '):

        #takesa bout 0.00099

        if(s.stop_word_type(word)==0):
            words.append(word)


    return  ' '.join(words)

tick = time.time()

yaqutz_pd = pd.read_excel('data/structured/FullYaqut.xlsx', sheet_name='ALL')

yaqutz_pd['Description'] = yaqutz_pd['Description'].apply(lambda x :clean_text(x))



yaqutz_pd['Description'] = yaqutz_pd['Description'].apply(lambda x :retrun_prers(x))
c = Counter()
df = yaqutz_pd['Description'].str.split(expand=True).stack().value_counts()
df.to_csv('prep_only.csv')
tack = time.time()
print(tack - tick)
print(df)

