import streamlit as st

import pandas as pd 

if "df" not in st.session_state:
    st.session_state.df = None

@st.cache_data
def load_csv(file):
    return file