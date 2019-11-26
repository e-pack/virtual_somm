# Import packages to analyze text
import nltk 
import re
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


# Open wine data and limit columns to Variety, Description
import pandas as pd
import numpy as np

df = pd.read_csv("wine_data.csv")
df = df[['variety','description']]

# Remove the author from the descriptions (last two words of description)
def remove_author(text):
    text = text.rsplit(' ', 2)[0]
    return text

df.description = df.description.apply(remove_author)


# Filter dataset for Cabernet Sauvignon, Chardonnay, Pinot Gris, Sauvignon Blanc, and Merlot
include_varieties = ['Cabernet Sauvignon','Chardonnay','Pinot Gris','Sauvignon Blanc','Merlot']
df = df[df.variety.isin(include_varieties)]

# Group DataFrame by variety
df = df.groupby(['variety'])['description'].apply(' '.join).reset_index()

# Data cleaning to make text lowercase, remove punctuation, etc. 
def clean_text_round1(text):
    text = text.lower()
    text = re.sub('\[.*?\]', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', ' ', text) 
    text = re.sub('[‘’“”…]', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('–', ' ', text)
    text = re.sub('—', ' ', text) 
    return text

round1 = lambda x: clean_text_round1(x)
df.description = df.description.apply(round1)

# Remove stop words ('the','a','an', etc.) and words that will not differentiate wines ('grape','fruit','nice')
stop_words = stopwords.words('english')

remove_words = pd.read_csv("remove_words.csv")
remove_words = remove_words['remove_words'].values
for words in remove_words:
    stop_words.append(words)

stemming = PorterStemmer()

def clean_text_round_2(row):
    description = row['description']
    tokens = nltk.word_tokenize(description)
    token_words = [w for w in tokens if w.isalpha()]
    stemmed_words = [stemming.stem(w) for w in token_words]
    meaningful_words = [w for w in token_words if not w in stop_words]
    #joined_words = (" ".join(meaningful_words))
    return meaningful_words

df['meaningful_words'] = df.apply(clean_text_round_2, axis=1)

df.to_csv('cleaned_wine_data.csv')







