import xmltodict
import pandas as pd
from farasa.stemmer import FarasaStemmer
from pyarabic.araby import strip_harakat
# with open('data/stopwords/VoweledToolwords.xml') as fd:
#     doc = xmltodict.parse(fd.read())

voweld_path = 'data/stopwords/VoweledToolwords.xml'
unvoweld_path = 'data/stopwords/UnvoweledToolwords.xml'
typs_path = 'data/stopwords/TypeToolwords.xml'

# for word in doc['toolwords']['toolword']:
#     print(word)

""" handles Place/Timer prepositions, we need this class, because its faster for the detection of prepositions in general   """


class Stopwords_Handler:
    def __init__(self, stem=False):

        with open(voweld_path) as fd:
            voweld_doc = xmltodict.parse(fd.read())
        with open(unvoweld_path) as fd:
            unvoweld_doc = xmltodict.parse(fd.read())
        with open(typs_path) as fd:
            typs_doc = xmltodict.parse(fd.read())

        self.voweled_df = pd.DataFrame.from_dict(voweld_doc['toolwords']['toolword'])
        self.unvoweled_df = pd.DataFrame.from_dict(unvoweld_doc['toolwords']['toolword'])
        self.types_df = pd.DataFrame.from_dict(typs_doc['types'])
        self.stem=stem
        if self.stem:
            self.stemmer = FarasaStemmer()

    """checks the relevent type of the word 
    there is 56 different types any 2 are relevent for now 
    returns: 0 - for place , 1 - for time """

    def stop_word_type(self, word):
        if self.stem:
           stemmed_word = self.stemmer.stem(word)
        else:
            stemmed_word = word
        try:
            word_ids = self.unvoweled_df.loc[self.unvoweled_df['@unvoweledform'] == stemmed_word]['@ids'].values[
                0].split(' ')
            voweled_words = self.voweled_df.loc[self.voweled_df['@id'].isin(word_ids)]
            if '50' in voweled_words['@type'].values:
                return 0
            if '49' in voweled_words['@type'].values:
                return 1
        except:
            return None
        return None



    """get all the Place prepostions """
    def get_all_place_pre(self):
        place_pre = self.voweled_df[self.voweled_df['@type']=='50']
        place_pre['@voweledform'] = place_pre['@voweledform'].apply(lambda x : strip_harakat(x))
        return  place_pre['@voweledform'].tolist()



    """get all the Time prepostions """
    def get_all_time_pre(self):
        time_pre = self.voweled_df[self.voweled_df['@type']=='49']
        time_pre['@voweledform'] = time_pre['@voweledform'].apply(lambda x : strip_harakat(x))
        return  time_pre['@voweledform'].tolist()


