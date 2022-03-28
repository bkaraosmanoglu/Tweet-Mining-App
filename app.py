#Burak
import streamlit as st
import tweetScrape
import tweetPreProcess   

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

PAGES = {
    "Tweet Query":tweetScrape,
    "Tweet Preprocess":tweetPreProcess,
}
st.sidebar.title('MENU')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()


