import os
import streamlit as st

from src.langgraph_agentic_bot_app.ui.streamlitui.uiconfigfile import Config

class LoadUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
        

    def get_user_controls(self)->dict:

        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")

        st.title("🤖 "+ self.config.get_page_title())

        with st.sidebar:

            llm_options = self.config.get_llms()
            self.user_controls['selected_llm'] = st.selectbox("Select your LLM", llm_options)

            if self.user_controls['selected_llm'] == "Groq":
                groq_model_options = self.config.get_groq_models()
                self.user_controls['selected_groq_model'] = st.selectbox("Select your groq model", groq_model_options)

                self.user_controls['groq_api_key']=st.session_state["GROQ_API_KEY"]=st.text_input("Enter your GROQ API KEY", type="password")

                if not self.user_controls['groq_api_key']:
                    st.error("⚠️ Error Occurred: Please Enter your GROQ API KEY to START")

            usecase_options = self.config.get_usecases()
            self.user_controls['selected_usecase'] = st.selectbox("Select Usecase", usecase_options)

        return self.user_controls       



