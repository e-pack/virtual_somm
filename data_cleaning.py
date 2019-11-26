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

df = pd.read_csv("wine_data_results.csv")
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
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text) 
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('–', '', text)
    text = re.sub('—', '', text) 
    text = re.sub('/(^| ).( |$)/', '$1', text)
    text = re.sub(r"\b[a-zA-Z]\b", "", text)
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

import plotly.express as px
from nltk import FreqDist

def max_freq(row):
    text = row['meaningful_words']
    fdist = FreqDist(text)
    return [(word, freq) for word, freq in fdist.most_common(30)]

df['common_descriptors'] = df.apply(max_freq, axis=1)

df = df[['variety','common_descriptors']]

frequency_table=pd.DataFrame()
for i in range (0,len(df.index)):
    data = df.iloc[i,1]
    variety = df.iloc[i,0]
    table = pd.DataFrame(data, columns = ['Word', 'word_frequency'])
    table['Variety'] = variety
    table = table[['Variety','Word','word_frequency']]
    frequency_table=frequency_table.append(table,ignore_index=True)

# Add columns to calculate percentage of descriptor words

frequency_table['total_occ'] = frequency_table.groupby('Variety')["word_frequency"].transform('sum')
frequency_table['percentage'] = (frequency_table['word_frequency']/frequency_table['total_occ'])*100




fig = px.scatter_polar(frequency_table, r="percentage", theta="Word", color="Variety",symbol="Variety",
                    color_discrete_sequence=px.colors.sequential.Plasma[-2::-1],
                    template="seaborn",width=1600,height=1600)

fig.show()







