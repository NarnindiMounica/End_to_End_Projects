from langchain_ollama import ChatOllama

from src.web_search_agentic_bot.tools.web_search_tools import ToolsNode

class OllamaModel:
    def __init__(self, user_controls):
        self.user_controls=user_controls

    def get_simple_ollama_model(self):
         
        model_type=self.user_controls['selected_ollama_model']  

        #initializing model
        model=ChatOllama(model=model_type)

        return model
    
    def get_web_search_tool_ollama_model(self):
        
        base_model = self.get_simple_ollama_model()
        tools_to_bind = ToolsNode().get_bind_tools()
        tools_bind_model = base_model.bind_tools(tools_to_bind)

        return tools_bind_model
    
