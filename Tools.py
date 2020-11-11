import pandas as pd
import re
from farasa.stemmer import FarasaStemmer
import string
import stop_words_handler
from string import digits
from string import ascii_letters as end_letters
from farasa.segmenter import FarasaSegmenter
# TODO: handle ambigouse Place Names
remove_digits = str.maketrans('', '', digits)

yaqutz_pd = pd.read_excel('data/structured/FullYaqut.xlsx', sheet_name='ALL')
yaqutz_pd_types = pd.read_excel('data/structured/FullYaqut.xlsx', sheet_name='Type')
yaqutz_pd_types = set(yaqutz_pd_types['Type_Arabic'])
stemmer = FarasaStemmer(interactive=True)
segmentor = FarasaSegmenter(interactive=True)
places = yaqutz_pd['PlaceName'].tolist()
s = stop_words_handler.Stopwords_Handler()


# unvoeweld = set(s.unvoweled_df['@unvoweledform'])


def search_place(palce):
    print("\n".join(s for s in places if palce in s))


def clean_text(sentence, hard=False):
    words = []

    if not hard:
        punc = '''</>~%#`÷×؛_()*&^%][ـ/"؟'{}~¦+|!”…“–ـ'''
        punc = punc + end_letters
    else:
        english_punctuations = string.punctuation
        arabic_punctuations = '''`÷×؛_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        punc = english_punctuations + arabic_punctuations

    for w in sentence.split(' '):

        # Cleaning Numbers
        w = w.translate(remove_digits)

        # Removing the punctuations
        for ch in punc:
            w = w.replace(ch, '')

        if any(sep in w for sep in ['.', '،', ':']):
            w = w[0:-2] + ' ' + w[-1]

        if not re.search(r'[a-zA-Z]', w):
            words.append(w)
    return ' '.join(words)


# def _fact_extractor(sentence):
#
#     index,start_index = 0,0
#     for word in sentence.split(' '):


def window_of_word(sentnce, word, window=1):
    index, start_index = 0, 0
    sentnce = sentnce.split(' ')

    if word in sentnce:
        index = [int(i) for i in range(len(sentnce)) if sentnce[i] == word]
        print(index)
        stride = ' | '
        for i in index:

            for k in range(window * 2 + 1):
                stride = stride + sentnce[i - window + k] + ' '
            stride = stride + " | "

        return stride
    else:
        return None


def filer_place_name(text):
    places = []
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
        if X:
            places.append(X[0][2:-1])
    with open('data/dumb/dev_palce_list.txt', 'w') as f:
        for item in places:
            f.write("%s\n" % item)


def gen_place():
    global place_names
    place_names = yaqutz_pd[yaqutz_pd['PlaceName'].apply(lambda x: len(x.split(' ')) < 2)]['PlaceName']
    place_names = set(place_names)
    # return _generate_place_relations()


def _generate_place_relations():
    df = yaqutz_pd[['Description', 'PlaceName']]
    df['Description'] = df['Description'].apply(lambda x: clean_text(x, hard=True))
    df['Relation_to'] = df['Description'].apply(lambda x: filer_place_name(x))
    df[['PlaceName', 'Relation_to']].to_csv('placce_names_relatios.csv')


def window_ofword_on_df(word):
    df = yaqutz_pd[['Description', 'PlaceName']]
    df['Description'] = df['Description'].apply(lambda x: clean_text(x, hard=True))
    df['Relation_to'] = df['Description'].apply(lambda x: window_of_word(x, word))
    df[['PlaceName', 'Relation_to']].to_csv(word + 'window_of_token.csv')


#
# gen_place()
def type_exists(type):
    return type in yaqutz_pd_types


def split_n_grams(n=3):
    df = yaqutz_pd
    for i in range(1, n + 1):
        df2 = yaqutz_pd[yaqutz_pd['PlaceName'].apply(lambda x: len(x.split(' ')) == i)]
        df2.to_csv('data/structured/' + str(i) + '- grams.csv')


def clean_df():
    # window_ofword_on_df('في')
    df = yaqutz_pd['Description']
    df = df.apply(lambda x: clean_text(x, hard=False))
    df.to_csv('clean_disc.csv')


def _TPP_recognition(text):
    entities = []
    entity = {}
    gen_place()

    for sentence in pattern.split(text):
        print(sentence)
        for word in sentence.split(' '):
            print(word)
            token = stemmer.stem(word)
            print(type_exists(token))
            print(token in place_names)
            print(s.stop_word_type(token))
            if (type_exists(token)):
                # TODO:
                entity['type'] = token
            if token in place_names:
                # TODO:
                entity['name'] = token
            if s.stop_word_type(token) == 1:
                # TODO:
                entity['s_prep'] = token
        if entity:
            entities.append(entity)
    return entities


print(_TPP_recognition(' بالجيم المكسورة والنون الساكنة وقاف وألف ونون : وهي قرية من قرى سرخس، ينسب إليها أبو الفضل محمد بن عبد الواحد الآجنقاني ، والعجم آجنكان .'))