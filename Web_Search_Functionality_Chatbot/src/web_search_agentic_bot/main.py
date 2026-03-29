import os
import streamlit as st

from src.web_search_agentic_bot.ui.streamlitui.loadui import LoadStreamlitUI
def get_websearch_bot():
    user_controls = LoadStreamlitUI().load_streamlit_ui()

    user_in= st.text_input("Enter your query")