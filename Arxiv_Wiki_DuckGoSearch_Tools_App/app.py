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
    st.sidebar.write("Model initialized successfully ✅")

    tools_agent = create_agent(model, 
                               tools=tools,
                               system_prompt="You are a answering tool, answer asked questions using only tools given")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"assistant",
                                      "content": "I am a text generating app, please enter a topic to get more info on it"}]

        for msg in st.session_state.messages:
            st.chat_message(msg['role']).write(msg['content'])

            if user_in:= st.chat_input(placeholder="what is agentic ai?"):
                st.session_state.messages.append({"role":"user", "content":user_in})
                st.chat_message("user").write(user_in)

                with st.chat_messages("assistant"):
                    st_callback  = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                    response = tools_agent.invoke(st.session_state.messages, callbacks=[st_callback])
                    st.session_state.messages.append({"role":"assistant", "content":response})
                    st.write(response)



