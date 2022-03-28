import datetime
import streamlit as st 
import nltk
from textblob import TextBlob
import pandas as pd
import re
import nltk
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist
import string
from datetime import date
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

current_date = datetime.datetime.now()
filename1 = str(current_date.day)+str(current_date.month)+str(current_date.year)+"twintMinOutputSentiment"

from datetime import date
today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")

def app():

    def textProcess(file):
        df_clean = pd.read_csv(file, encoding='utf-8')
        df_clean.drop(df_clean.columns.difference(['username','date','language','hashtags','tweet']), 1, inplace=True)
        # lower case
        df_clean["tweet"] = df_clean["tweet"].str.lower()
        # remove url links
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r'https?:\/\/\S+', '', x))
        # remove url/website that didn't use http, is only checking for .com websites 
        # so words that are seperated by a . are not removed
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', x))
        # remove @mention
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r'@mention', '', x))
        # remove {link}
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r'{link}', '', x))
        # remove &text; html chars
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r'&[a-z]+;', '', x))
        # [video]   
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"\[video\]", '', x))
        # remove all remaining characters that aren't letters, white space, or 
        # the following #:)(/\='] that are used in emojis or hashtags
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"[^a-z\s\(\-:\)\\\/\];='#]", '', x))
        # correcting the abbreviations
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"what's", "what is ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"\'ve", " have ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"n't", " not ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"i'm", "i am ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"\'re", " are ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"\'d", " would ", x))
        df_clean["tweet"] = df_clean["tweet"].apply(lambda x: re.sub(r"\'ll", " will ", x))
        
        tknzr = TweetTokenizer()
        df_clean['tokens'] = df_clean['tweet'].apply(tknzr.tokenize)
        nltk.download('stopwords')
        stop = stopwords.words('english')
        df_clean['tokens'] = df_clean['tokens'].apply(lambda x: [item for item in x if item not in stop])
        PUNCUATION_LIST = list(string.punctuation)
        def remove_punctuation(word_list):
            """Remove punctuation tokens from a list of tokens"""
            return [w for w in word_list if w not in PUNCUATION_LIST]
        df_clean['tokens'] = df_clean['tokens'].apply(remove_punctuation)
        df_clean.to_csv("Clean"+file,encoding='utf-8')
        corpus_tokens = df_clean['tokens'].sum()
        corpus_freq_dist = FreqDist(corpus_tokens)
        for_charts = corpus_freq_dist.most_common(20)
        for_pie = corpus_freq_dist.most_common(10)
        for_words = corpus_freq_dist.most_common(100)
        for_words = pd.Series(dict(for_words))
        for_words = for_words.to_frame()
        col1, col2 = st.beta_columns(2)

        ## Conversion to Pandas series via Python Dictionary for easier plotting
        for_charts = pd.Series(dict(for_charts))
        for_pie = pd.Series(dict(for_pie))
        ## Setting figure, ax into variables
        fig5, ax = plt.subplots(figsize=(10,10))
        
        ## Seaborn plotting using Pandas attributes + xtick rotation for ease of viewing
        # all_plot = 
        plt.title('Analysis '+file)
        plt.xlabel('word')
        plt.ylabel('count')
        sns.barplot(x=for_charts.index, y=for_charts.values, ax=ax)
        plt.xticks(rotation=90)
        with col1:
            st.pyplot(fig5)
        plt.savefig(file+'BarPlot.png')
        fig6, ax1 = plt.subplots()
        myexplode = [0.3, 0.2, 0.2, 0.2,0.1,0.1,0.1,0.1,0.1,0.1]
        plt.title('Analysis '+file)
        ax1.pie(for_pie.values, labels =for_pie.index , explode = myexplode, shadow = True, autopct='%1.0f%%')
        with col2:
            st.pyplot(fig6)
        plt.savefig(file+'PieChart.png')

        df_clean['polarity'] = df_clean.apply(lambda x: TextBlob(x['tweet']).sentiment[0], axis=1)
        df_clean['subjectivity'] = df_clean.apply(lambda x: TextBlob(x['tweet']).sentiment[1], axis=1)
        df_clean['sentiment'] = df_clean['polarity'].apply(lambda x: 'Positive' if x>0 else ('Negative' if x<0 else 'Neutral'))
        df_clean.to_csv("Sentiment"+file, encoding='utf-8')
        df_clean = pd.read_csv("Sentiment"+file, encoding='utf-8')
        fdist = FreqDist(df_clean['sentiment'])
        fdist = pd.Series(dict(fdist))
        
        col3, col4 = st.beta_columns(2)

        fig8, ax3 = plt.subplots()
        ## Seaborn plotting using Pandas attributes + xtick rotation for ease of viewing
        # all_plot = 
        plt.title('Sentiment Analysis'+file)
        plt.xlabel('sentiment')
        plt.ylabel('count')
        sns.barplot(x=fdist.index, y=fdist.values)
        plt.xticks(rotation=90)
        with col3:
            st.pyplot(fig8)

        fig7,ax2 = plt.subplots()
        plt.title("Sentiment Analysis"+file)
        ax2.pie(fdist.values, labels =fdist.index , shadow = True, autopct='%1.0f%%')
        with col4:
            st.pyplot(fig7)
        plt.savefig(file+'sentimentPieChart.png')
        for_words.to_csv("dataframe"+file)
        st.dataframe(for_words)

    def main():
        html_temp = """
        <h2 style="color:red;text-align:center;"> Tweet Preprocess and Sentiment Analysis </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        st.markdown("Upload your file to text preprocess and sentiment analysis")
        file = st.file_uploader("Choose a file")
        if st.button("Text Preprocess and Sentiment Analysis"):
            textProcess(file)
        
    main()