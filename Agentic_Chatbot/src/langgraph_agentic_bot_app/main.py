import os
import streamlit as st

from src.langgraph_agentic_bot_app.ui.loadui import LoadUI
from src.langgraph_agentic_bot_app.llms.groqllm import GroqLLM
from src.langgraph_agentic_bot_app.graphs.graph_builder import GraphSelector
from src.langgraph_agentic_bot_app.ui.displayui import DisplayResults



def langgraph_agentic_bot():
    """
    Docstring for langgraph_agentic_bot

    this function

    """
    try:
        ui = LoadUI()
        user_controls = ui.get_user_controls()

    except Exception as e:
        print(f"🔴 Error Occurred while loading user controls: {e}" ) 

    usecase  = user_controls['selected_usecase']   

    user_message = st.chat_input("Enter your message..")

    if user_message:

        try:
            
            if user_controls['selected_llm'].lower()=="groq":
                model = GroqLLM(user_inputs=user_controls).get_groq_llm()

        except Exception as e:
            print(f"🔴 Error Occurred while initializing llm model: {e}" ) 

        try:

            graph_selector = GraphSelector(model=model)

            graph = graph_selector.select_graph(usecase=usecase)

        except Exception as e:
            print(f"🔴 Error Occurred while selecting graph for the usecase {usecase}: {e}" ) 

        try:

            display_result = DisplayResults(graph=graph, usecase=usecase, user_message=user_message)  

            ui_display = display_result.display_ui() 

            return ui_display

        except Exception as e:

            print(f"🔴 Error Occurred while displaying results on streamlit ui: {e}" )  

            return    






    

        

    