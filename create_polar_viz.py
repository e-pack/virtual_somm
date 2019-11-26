# Create polar vizualization for each varietal 
import pandas as pd
import plotly.express as px
from nltk import FreqDist


df = pd.read_csv('cleaned_wine_data.csv')

def max_freq(row):
    text = row['meaningful_words']
    fdist = FreqDist(text)
    return [(word, freq) for word, freq in fdist.most_common(20)]

df['common_descriptors'] = df.apply(max_freq, axis=1)


df_test = df[['variety','common_descriptors']]

print(df_test['common_descriptors'])

final_table=pd.DataFrame()
for i in range (0,len(df.index)):
    data = df_test.iloc[i,1]
    variety = df_test.iloc[i,0]
    table = pd.DataFrame(data, columns = ['Word', 'Frequency'])
    table['Variety'] = variety
    table = table[['Variety','Word','Frequency']]
    final_table=final_table.append(table,ignore_index=True)


fig = px.line_polar(final_table, r="Frequency", theta="Word", color="Variety", line_close=True,
                    color_discrete_sequence=px.colors.sequential.Plasma[-2::-1],
                    template="seaborn")

fig.show()