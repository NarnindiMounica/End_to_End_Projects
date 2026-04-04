import streamlit as st
import os

from src.web_search_agentic_bot.ui.uiconfigfile import Config

class LoadStreamlitUI:

    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):

        st.set_page_config(page_title="👨‍💻🎧 "+ self.config.get_page_title())  
        st.title("👨‍💻🎧 "+ self.config.get_page_title()) 

        with st.sidebar:
            model_options = self.config.get_models()
            self.user_controls['selected_model']=st.selectbox("Select your model", model_options) 

            if self.user_controls['selected_model']=="Groq":
                groq_model_options = self.config.get_groq_model_types()
                self.user_controls['selected_groq_model']=st.selectbox("Select Groq model type", groq_model_options)
                self.user_controls['groq_api_key']=st.text_input("Enter your GROQ API Key", type="password") 
                if not self.user_controls['groq_api_key']:
                    st.warning(" ⚠️ Please enter GROQ API Key to proceed")
            elif self.user_controls['selected_model']=="Ollama":
                ollama_model_options = self.config.get_ollama_model_types()
                self.user_controls['selected_ollama_model']=st.selectbox("Select Ollama model type", ollama_model_options)

            usecase_options = self.config.get_usecases()
            self.user_controls['selected_usecase'] = st.selectbox("Select a Usecase", usecase_options) 

            if self.user_controls['selected_usecase']=="Web Search" or self.user_controls['selected_usecase']=="AI News Summary":
                os.environ['TAVILY_API_KEY']=self.user_controls['TAVILY_API_KEY']=st.text_input("Enter your Tavily API Key",type="password")

            if self.user_controls['selected_usecase']=="AI News Summary":
                st.subheader("Get AI News")
                self.user_controls['selected_time_frame'] =st.selectbox("⏳ Select Time Frame To Get AI News", ['Daily', 'Weekly', 'Monthly'])

                if st.button("Fetch AI News 🔎"):
                    st.session_state['time_frame']=self.user_controls['selected_time_frame']


        return self.user_controls    



