from langchain_groq import ChatGroq

class GroqModel:
    def __init__(self, user_controls):
        self.user_controls=user_controls

    def get_simple_groq_model(self):
        groq_api_key=self.user_controls['groq_api_key']  
        model_type=self.user_controls['selected_groq_model']  

        #initializing model
        model=ChatGroq(api_key=groq_api_key, model=model_type)

        return model