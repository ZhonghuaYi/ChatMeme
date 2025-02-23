import streamlit as st

pg = st.navigation([
    st.Page("pages/meme_search.py"),
    st.Page("pages/config.py"),
    st.Page("pages/meme_library.py")
])
pg.run()