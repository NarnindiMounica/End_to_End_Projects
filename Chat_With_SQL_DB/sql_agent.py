import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

st.title("SQL Agent")

#llm model
llm = init_chat_model(model="groq:llama-3.1-8b-instant", api_key=groq_api_key)