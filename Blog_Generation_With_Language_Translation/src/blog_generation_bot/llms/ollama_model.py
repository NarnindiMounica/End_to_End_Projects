from langchain_ollama import ChatOllama

class OllamaModel:

    def get_ollama_model(self):

        model = ChatOllama(model="minimax-m2.7:cloud")

        return model