import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain.agents import create_agent, AgentState

from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun, ArxivQueryRun, WikipediaQueryRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

st.title("Generate Answer Using Arxiv, Wikipedia and DuckDuckGoSearch Engines")

#defining tools

arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500))
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500))
duck_search = DuckDuckGoSearchRun()

tools = [arxiv, wikipedia, duck_search]

groq_api_key = st.sidebar.text_input("Enter your model api keys", type="password")
if groq_api_key:
    model = ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")
    st.sidebar.success("Model initialized successfully")

    tools_agent = create_agent(model=model, 
                               tools=tools)
    
    #initializing messages
    if "messages" not in st.session_state:
        st.session_state['messages']=[{"role":"assistant", "content":"I'm a generating app, please enter your topic to present some info on it"}]
        st.chat_message("assistant").write(st.session_state['messages'][0]['content'])

    #appending user messages
    user_in = st.chat_input(placeholder="what is gen ai")
    if user_in:
        st.session_state['messages'].append({"role":"user", "content":user_in}) 
        response = tools_agent.invoke({"messages": st.session_state['messages'][-1] })
        st.session_state['messages'].append({"role":"assistant", "content":response['messages'][-1].content}) 

    #to display
    for msg in st.session_state['messages'][1:]:
        if msg['role']=="assistant":
            st.chat_message("assistant").write(msg['content'])
        else:
            st.chat_message("user").write(msg['content'])

                 

