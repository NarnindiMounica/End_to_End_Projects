import os
import streamlit as st
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage

class DisplayStreamlitUI:
    def __init__(self, graph, usecase, user_message):
        self.graph = graph
        self.usecase = usecase
        self.user_message = user_message

    def display_streamlit_ui(self):
        graph = self.graph
        usecase = self.usecase
        user_message = self.user_message

        if usecase.lower()=="generic search":
            for event in graph.stream({'messages': user_message}, stream_mode="values"):
                print(event.values())

            with st.chat_message("user"):
                st.write(user_message)
            with st.chat_message("assistant"):
                st.write(event['messages'][-1].content) 

        elif usecase.lower()=="web search":
            response = graph.invoke({'messages': user_message})
            
            for message in response['messages']:
                if type(message)==HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                else:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase.lower()=="ai news summary":
            frequency = self.user_message
            with st.spinner("⏳Fetching and Summarizing News"):
                response = graph.invoke({'messages': frequency})
                try:
                    #reading markdown file
                    file_path = f"D:\\End_To_End_Projects\\Web_Search_Functionality_Chatbot\\AI_News\\{frequency}_summary.md"
                    with open(file_path, "r") as f:
                        markdown_content=f.read()

                    #displaying markdown content in streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News not generated or file not found:{file_path}") 
                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")           



