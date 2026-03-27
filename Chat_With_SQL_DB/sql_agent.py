import os
import sqlite3
import streamlit as st
from pprint import pprint
from dotenv import load_dotenv
from pathlib import Path
from langchain.agents import create_agent
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

    #creating agent with system prompt
    system_prompt = """
        You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run,
        then look at the results of the query and return the answer. Unless the user
        specifies a specific number of examples they wish to obtain, always limit your
        query to at most {top_k} results.

        You can order the results by a relevant column to return the most interesting
        examples in the database. Never query for all the columns from a specific table,
        only ask for the relevant columns given the question.

        You MUST double check your query before executing it. If you get an error while
        executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
        database.

        To start you should ALWAYS look at the tables in the database to see what you
        can query. Do NOT skip this step.

        Then you should query the schema of the most relevant tables.
        """.format(
            dialect=local_db.dialect,
            top_k=5,
        )
    
    agent= create_agent(
        model=llm,
        tools=db_tools,
        system_prompt=system_prompt
    )

    #running agent
    user_query=st.text_input("Please ask your query here")
    if user_query:
        for event in agent.stream({"messages":[{"role":"user", "content":user_query}]}, stream_mode="updates"):
            st.success(event)
    






