import os
import streamlit as st
import validator
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import load_summarize_chain


st.title("➡️Summarize Youtube Video Transcript or URL🌍")

