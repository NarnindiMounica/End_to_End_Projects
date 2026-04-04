import os
import streamlit as st

from src.web_search_agentic_bot.ui.streamlitui.loadui import LoadStreamlitUI
from src.web_search_agentic_bot.ui.streamlitui.displayui import DisplayStreamlitUI
from src.web_search_agentic_bot.llms.groq_model import GroqModel
from src.web_search_agentic_bot.llms.ollama_model import OllamaModel
from src.web_search_agentic_bot.graphs.bot_graph import SelectGraph

def get_websearch_bot():
    user_controls = LoadStreamlitUI().load_streamlit_ui()

    if user_controls['fetch_ai_news'] is not " ":
        user_message = user_controls['time_frame']
    else:    
        user_message= st.text_input("Enter your query")


    if user_message:

        usecase = user_controls['selected_usecase']
        if user_controls['selected_model']=="Groq":
            if usecase.lower()=="generic search" or usecase.lower()=="ai news summary":
                model_obj = GroqModel(user_controls=user_controls).get_simple_groq_model()
            elif usecase.lower()=="web search":
                model_obj = GroqModel(user_controls=user_controls).get_web_search_tool_groq_model() 

        elif user_controls['selected_model']=="Ollama":
            if usecase.lower()=="web search" or usecase.lower()=="ai news summary":
                model_obj = OllamaModel(user_controls=user_controls).get_simple_ollama_model() 
            elif usecase.lower()=="web search":
                model_obj = OllamaModel(user_controls=user_controls).get_web_search_tool_ollama_model()      

        graph_obj = SelectGraph(model=model_obj)
        
        usecase_graph_obj = graph_obj.get_usecase_graph(usecase=usecase)

        display_ui_obj = DisplayStreamlitUI(graph=usecase_graph_obj, usecase=usecase, user_message=user_message)
            
        display_ui_obj.display_streamlit_ui()

        
