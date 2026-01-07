from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_inputs:dict):
        self.user_inputs= user_inputs

    def get_groq_llm(self):
        """Initialize and return a Groq LLM client using the specified model and API key."""
        model =  ChatGroq(
            model=self.user_inputs['selected_groq_model'],
            groq_api_key=self.user_inputs['groq_api_key']
        )  

        return model
