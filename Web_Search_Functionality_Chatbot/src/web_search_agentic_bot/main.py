import os
import streamlit as st

from src.web_search_agentic_bot.ui.streamlitui.loadui import LoadStreamlitUI
from src.web_search_agentic_bot.ui.streamlitui.displayui import DisplayStreamlitUI
from src.web_search_agentic_bot.llms.groq_model import GroqModel
from src.web_search_agentic_bot.llms.ollama_model import OllamaModel
from src.web_search_agentic_bot.graphs.bot_graph import SelectGraph

def get_websearch_bot():
    user_controls = LoadStreamlitUI().load_streamlit_ui()

    user_message= st.text_input("Enter your query")

    if user_message:
        if user_controls['selected_model']=="Groq":
            model_obj = GroqModel(user_controls=user_controls).get_simple_groq_model()
            graph_obj = SelectGraph(model=model_obj)
            usecase = user_controls['selected_usecase']
            usecase_graph_obj = graph_obj.get_usecase_graph(usecase=usecase)

            display_ui_obj = DisplayStreamlitUI(graph=usecase_graph_obj, usecase=usecase, user_message=user_message)
            
            display_ui_obj.display_streamlit_ui()

        
