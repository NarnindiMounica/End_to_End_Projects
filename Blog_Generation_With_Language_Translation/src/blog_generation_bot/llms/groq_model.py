import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class GroqModel:

    def get_groq_model(self):

        model = ChatGroq(model="llama-3.1-8b-instant")

        return model