import os
import streamlit as st
import validator
from langchain_groq import ChatGroq
from langchain import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader