from configparser import ConfigParser

class Config:
    def __init__(self, file_name="D:\\End_To_End_Projects\\Web_Search_Functionality_Chatbot\\src\\web_search_agentic_bot\\ui\\streamlitui\\uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(file_name)

    def get_page_title(self):
        page_title = self.config['DEFAULT'].get("PAGE_TITLE")
        return page_title
    
    def get_models(self):
        model_options = self.config['DEFAULT'].get("MODELS").split(", ")
        return model_options
    
    def groq_model