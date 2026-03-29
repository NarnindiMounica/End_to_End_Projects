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
        print(db_filepath)
        creator = lambda : sqlite3.connect(f"file:{db_filepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_url==radio_options[1]:
        if not (mysql_host and mysql_db and mysql_username and mysql_userpassword):
            return None
        else:
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_username}:{mysql_userpassword}@{mysql_host}/{mysql_db}"))
        
if db_url==radio_options[1]:
    if  (db_host and db_userdb and db_username and db_userpassword ):
        db=configure_db(db_url, db_host, db_userdb, db_username, db_userpassword)
    else:
        st.error("Please enter all MySQL Connection details")
        st.stop()
elif db_url==radio_options[0]:
    db=configure_db(db_url)
else: 
    st.error("Database Connection Failed")
    st.stop()

#toolkit configuration
db_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = db_toolkit.get_tools()

#creating mysql agent
agent = create_sql_agent(
    llm=llm,
    toolkit=db_toolkit,
    verbose=True
)

#conversation messages

if "messages" not in st.session_state or st.sidebar.button("Clear Conversation History"):
    st.session_state['messages']=[{"role":"assistant", "content":"Hello, How can I help you?"}]

#displaying past converstaion if any
for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

#getting user query
user_in=st.chat_input("Please ask your query here..")

if user_in:
    st.session_state['messages'].append({"role":"user", "content":user_in})
    st.chat_message("user").write(user_in)

    response=agent.run(user_in)
    st.session_state['messages'].append({"role":"assistant", "content": response})
    st.success(response)



