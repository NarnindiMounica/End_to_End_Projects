from langchain_ollama import ChatOllama

class OllamaModel:
    def __init__(self, user_controls):
        self.user_controls=user_controls

    def get_simple_ollama_model(self):
         
        model_type=self.user_controls['selected_ollama_model']  

        #initializing model
        model=ChatOllama(model=model_type)

        return model