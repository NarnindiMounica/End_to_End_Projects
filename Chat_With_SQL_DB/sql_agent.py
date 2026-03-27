import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit


load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")

st.title("SQL Agent")

#llm model
llm = init_chat_model(model="groq:llama-3.1-8b-instant", api_key=groq_api_key)

#creating a db connection
def configure_db(db_file):
    file_path = Path(db_file)
    db = SQLDatabase.from_uri(f"sqlite:///{file_path}")
    return db

db_file_from_user=st.text_input("Enter DB file name:")
if db_file_from_user:
    local_db= configure_db(db_file_from_user)
    st.write(f"Dialect: {local_db.dialect}")
    st.write(f"Available Tables: {local_db.get_usable_table_names()}")

    #adding tools for database interaction
    db_toolkit = SQLDatabaseToolkit(db=local_db, llm=llm)   

    db_tools = db_toolkit.get_tools()
    for tool in db_tools:
        st.write(f"Tool: {tool.name} Tool Description:{tool.description}\n\n ")


