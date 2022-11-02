import re
import nltk
import pandas as pd
from unicodedata import normalize
nltk.download('stopwords')
nltk.download('wordnet')


class pre_process_text:
  
    def __init__(self,flg_stemm=True, flg_lemm=False, stopwords_language=None):

        '''
        flg_stemm - choose to perform stemming pre treatment (True)
        flg_lemm - choose to perform lemmatization pre treatment (True)
        stopwords_language - select language to download stopwords (english,portuguese,german) if None dont perform selection
        '''

        #Get list of stopwords
        if stopwords_language:

            self.lst_stopwords = nltk.corpus.stopwords.words(stopwords_language) 

        else:

            self.lst_stopwords = False

        ## Stemming (remove -ing, -ly, ...)
        if flg_stemm == True:
            
            self.treat = nltk.stem.porter.PorterStemmer().stem

        else:

            self.treat = False

                    
        ## Lemmatisation (convert the word into root word)
        if flg_lemm == True:

            self.treat = nltk.stem.wordnet.WordNetLemmatizer().lemmatize

        else:

            self.treat = False


    @staticmethod
    def extract_string(regex_str,word):


        unit = re.findall(regex_str,word)
                                                
        if unit:

            return unit[0]

        else:

            return np.nan

    def transform(self,word):

        #Lower case letters

        word = word.lower()

        #Remove special char

        word = normalize('NFKD', word).encode('ASCII', 'ignore').decode('ASCII')

        #Remove punctuation

        word = re.sub(r'[^\w\s]', ' ',word)

        #Remove multiple Spaces

        word = re.sub(r'\s+', ' ',word)

        #Fix unit measures

 
        unit = self.extract_string(r'(\d+kg|\d+mg|\d+ml|\d+km|\d+cm|\d+meia|\d+w[\s\S]*?|\d+v[\s\S]*?|\d+g[\s\S]*?|\d+k[\s\S]*?|\d+l[\s\S]*?|\d+\s+g[\s\S]*?|\d+\s+k[\s\S]*?|\d+\s+kg|\d+\s+mg|\d+\s+ml|\d+\s+meia|\d+\s+km|\d+\s+cm|\d+\s+m[\s\S]*?|\d+\s+v[\s\S]*?|\d+\s+w[\s\S]*?)',word)

        if unit != unit:

            unit = self.extract_string(r'[\s\S]*?(\bkg)',word)

        if unit == unit:

            valor = self.extract_string(r'(\d+)',unit)
            unit_dim = self.extract_string(r'(\D+)',unit)

            if valor == valor:

                valor = re.sub(r'\s+', '',valor)

            else:

                valor = ''

            if unit_dim == unit_dim:

                unit_dim = re.sub(r'\s+', '',unit_dim)

            else:

                unit_dim = ''

            if unit =='meia':

                unit = self.extract_string(r'(\d+kg|\d+mg|\d+ml|\d+km|\d+cm|\d+w[\s\S]*?|\d+v[\s\S]*?|\d+g[\s\S]*?|\d+k[\s\S]*?|\d+l[\s\S]*?|\d+\s+g[\s\S]*?|\d+\s+k[\s\S]*?|\d+\s+kg|\d+\s+mg|\d+\s+ml|\d+\s+km|\d+\s+cm|\d+\s+v[\s\S]*?|\d+\s+w[\s\S]*?)',word)

                if unit != unit:

                    unit = 'meia'

                
                valor = self.extract_string(r'(\d+)',unit)
                unit_dim = self.extract_string(r'(\D+)',unit)

                if valor == valor:

                    valor = re.sub(r'\s+', '',valor)

                else:

                    valor = ''

                if unit_dim == unit_dim:

                    unit_dim = re.sub(r'\s+', '',unit_dim)

                else:

                    unit_dim = ''
            

            if valor == '':

                pass

            elif float(valor)>10000:

                valor = ''

            elif float(valor)<2 and unit == 'k':

                unit = 'kg'

            if valor == '' and unit != 'meia':

                unit_final = ' ' + '1' + unit_dim + ' '

            else:

                unit_final = ' ' + valor + unit_dim + ' '

        else:

            unit_final = None

        if unit_final:

            word = word.replace(unit,unit_final)

        #Remove multiple Spaces

        word = re.sub(r'\s+', ' ',word)

        #Remove single chars

        word = re.sub(r'\b\D\s\b', '',word)

        lst_text = word.split(' ')

        ## remove Stopwords
        if self.lst_stopwords:
            lst_text = [text for text in lst_text if text not in 
                        self.lst_stopwords]
                    
        
        if self.treat :

            lst_text = [self.treat(text) for text in lst_text]
                    
        ## back to string from list
        word = ' '.join(lst_text)

        return word
