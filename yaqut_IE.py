import pandas as pd
import re
from farasa.stemmer import FarasaStemmer
import string
import stop_words_handler





yaqutz_pd = pd.read_excel('data/structured/FullYaqut.xlsx', sheet_name='ALL')

# stemmer = FarasaStemmer(interactive=True)
places = yaqutz_pd['PlaceName'].tolist()
s = stop_words_handler.Stopwords_Handler()
unvoeweld = set(s.unvoweled_df['@unvoweledform'])



def search_place(palce):

    print("\n".join(s for s in places if palce in s))

def clean_text(w,hard=False):


    if not hard:
        punc =  '''#`÷×؛<>_()*&^%][ـ/"؟'{}~¦+|!”…“–ـ'''
    else:
        english_punctuations = string.punctuation
        arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        punc= english_punctuations+arabic_punctuations

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
    return w

def window_of_word(sentnce,word):
    window = 5
    index,start_index = 0,0
    sentnce = sentnce.split(' ')



    if word in sentnce :
        index = [i for i in range(len(sentnce)) if sentnce[i]== word]
        # print(len(index)>1)

        index =index[-1]

    for _ in range(index):

        if ':' in [char for char in sentnce[mark]]:
            start_index = mark + 1
            break
        mark -= 1
        if mark == 0 :
            start_index = index - window
    mark = index
    for _ in  range(len(sentnce)-index):
        if '،' in [char for char in sentnce[mark]]:
            end_index = mark + 1
            break
        end_index = index - window
        mark += 1

    sub_string = sentnce[start_index:end_index]

    # if ':' in sentnce:
    #     start_index = [i for i in range(len(sentnce)) if sentnce[i]==':'][0]
    #

    return ' '.join(sub_string)


def filer_place_name(text):

    places=[]
    # tolkens = stemmer.stem(text)
    for tolken in text.split(' '):
        if tolken in place_names:
            if tolken not in unvoeweld:
                places.append(tolken)
    return places

"""return regex matches for dev purposes"""
def _dev_regex_retriver():
    places = []
    book_as_txt = 'data/unstructured/0626YaqutHamawi.MucjamBuldan.Shamela0023735-ara1.txt'
    with open(book_as_txt) as text_file:
        moojam_alboldan = text_file.read()
    for line in moojam_alboldan.splitlines():
        X = re.findall(r"\$.*:$", line)
        if  X :
            places.append(X[0][2:-1])
    with open('data/dumb/dev_palce_list.txt', 'w') as f :
        for item in places:
            f.write("%s\n" % item)




def gen_place():
    global place_names
    place_names = yaqutz_pd[yaqutz_pd['PlaceName'].apply(lambda x : len(x.split(' ')) < 2)]['PlaceName']
    place_names = set(place_names)
    return _generate_place_relations()

def _generate_place_relations():

    df = yaqutz_pd[['Description','PlaceName']]
    df['Description'] = df['Description'].apply(lambda x:clean_text(x,hard=True))
    df['Relation_to'] = df['Description'].apply(lambda x: filer_place_name(x))
    df[['PlaceName','Relation_to']].to_csv('placce_names_relatios.csv')


#
# gen_place()

