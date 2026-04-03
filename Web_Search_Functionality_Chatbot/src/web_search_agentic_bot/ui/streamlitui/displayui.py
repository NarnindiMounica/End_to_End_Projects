import os
import streamlit as st

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
            for event in graph.stream({'messages': user_message}, stream_mode="values"):
                print(event.values())

            with st.chat_message("user"):
                st.write(user_message)
            with st.chat_message("assistant"):
                st.write(event['messages'][-1])          


