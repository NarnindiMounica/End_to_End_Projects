import os
import streamlit as st
import langchain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv

load_dotenv()

os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_v2']="true"
os.environ['LANGCHAIN_PROJECT']=os.getenv("LANGCHAIN_PROJECT")

st.title("❓ Q&A CHATBOT 🤖")

def get_response(model_type, api_key, temperature,):

    if api_key:
        llm = ChatGroq(model=model_type, api_key=groq_api_key, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "you are a q&a chatbot, answer precisely to asked question."),
            ("user", "{question}")

        ])

        chain  = prompt | llm | StrOutputParser()

        user_in = st.text_input("Please enter your query here...")
        if user_in:
            response = chain.invoke({"question":user_in})
            st.write(response)

model_type = st.sidebar.text_input("Enter model name:")

groq_api_key = st.sidebar.text_input("Enter api key:", type="password")

temperature = st.sidebar.slider("Set model temperature:", 0.0, 2.0, 0.3)

if __name__=="__main__":
    get_response(model_type=model_type, api_key=groq_api_key, temperature=temperature)

      


