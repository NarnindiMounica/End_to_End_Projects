from configparser import ConfigParser

class Config:
    def __init__(self, config_file="D:\\End_To_End_Projects\\Agentic_Chatbot\\src\\langgraph_agentic_bot_app\\ui\\streamlitui\\uiconfigfile.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self):
        return self.config['DEFAULT'].get("PAGE_TITLE")
    
    def get_llms(self):
        llm_options = self.config['DEFAULT'].get("LLMS").split(",")
        return llm_options
    
    def get_groq_models(self):
        groq_model_options = self.config['DEFAULT'].get("GROQ_MODELS").split(",")
        return groq_model_options
    
    def get_usecases(self):
        usecase_options = self.config['DEFAULT'].get("USECASES").split(",")
        return usecase_options


