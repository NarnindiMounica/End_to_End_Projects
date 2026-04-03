from langchain_groq import ChatGroq

from src.web_search_agentic_bot.tools.web_search_tools import ToolsNode

class GroqModel:
    def __init__(self, user_controls):
        self.user_controls=user_controls

    def get_simple_groq_model(self):
        groq_api_key=self.user_controls['groq_api_key']  
        model_type=self.user_controls['selected_groq_model']  

        #initializing model
        model=ChatGroq(api_key=groq_api_key, model=model_type)

        return model
    
    def get_web_search_tool_groq_model(self):
        
        base_model = self.get_simple_groq_model()
        tools_to_bind = ToolsNode().get_bind_tools()
        tools_bind_model = base_model.bind_tools(tools_to_bind)

        return tools_bind_model


