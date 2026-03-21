import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain.agents import create_agent, AgentState

from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun, ArxivQueryRun, WikipediaQueryRun

st.title("Generate Answer Using Arxiv, Wikipedia and DuckDuckGoSearch Engines")

groq_api_key = st.sidebar.text_input("Enter your model api keys", type="password")
if groq_api_key:
    model = ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")
    st.sidebar.write("Model initialized successfully ✅")
