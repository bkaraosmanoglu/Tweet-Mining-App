import twint
import datetime
import streamlit as st 
from st_aggrid import AgGrid
import nltk
import pandas as pd
import nltk
nltk.download('stopwords')

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

def app():

    def main():
        html_temp = """
        <h2 style="color:red;text-align:center;"> Tweet Query </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        words = st.text_input("HashTag or Text","Type Here")
        
        column1, column2 = st.columns(2)
        with column1:
            sinceInput = st.date_input("Since",datetime.date(2021, 1, 1))
            since=str(sinceInput)
        with column2:
            untilInput = st.date_input("Until")
            until=str(untilInput)
        likes = st.slider("How many minimum likes", 0, 500)
        replies = st.slider("How many minimum replies", 0, 500)
        retweets = st.slider("How many minimum retweets", 0, 500)
        limit = st.slider("Tweet Limit", 0, 100000, 10000)
        filename1 = st.text_input("Name of the file","Type Here")
        if st.button("Scrape", key="button1"):
            filename1
            c = twint.Config()
            c.Search = words
            c.Lang = "en"
            c.Limit = limit
            c.Since = since
            c.Until = until
            c.Min_likes = likes
            c.Min_replies = replies
            c.Min_retweets = retweets
            c.Store_csv = True
            c.Output = (filename1+".csv")
            twint.run.Search(c)
            st.write(since)
            st.write(until)
            st.write(likes)
            st.write(limit)
            
        if st.button("Output",key="button4"):
            dataset = pd.read_csv(filename1+".csv", encoding='utf-8')
            AgGrid(dataset)  

    main()