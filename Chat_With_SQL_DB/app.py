import os
import streamlit as st
import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from pathlib import Path
from langchain_cohere.sql_agent.agent import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

load_dotenv()

st.title("Query Your SQL DB 🛢️")

LOCAL_DB="local_db"
MYSQL_DB="mysql_db"

radio_options = [LOCAL_DB, MYSQL_DB]

st.sidebar.title("Selection Tab")
selected_db=st.sidebar.radio("Select your DB to query", radio_options)

if selected_db==radio_options[0]:
    db_url=LOCAL_DB
else:
    db_url=MYSQL_DB
    db_username=st.sidebar.text_input("MYSQL User")
    db_userpassword=st.sidebar.text_input("MYSQL User Password", type="password")
    db_userdb=st.sidebar.text_input("MYSQL Database")
    db_host=st.sidebar.text_input("MYSQL Host")

groq_api_key=st.sidebar.text_input("enter your model api key", type="password") 

if not groq_api_key:
    st.warning("Enter API Key ⚠️")

if not db_url:
    st.warning("No DB Selected ⚠️")    

#defining model
llm = ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")

@st.cache_resource(ttl="2h")
def configure_db(db_url, mysql_host=None, mysql_db=None, mysql_username=None, mysql_userpassword=None):
    if db_url==radio_options[0]:
        db_filepath=(Path(__file__).parent/"students.db").absolute()

