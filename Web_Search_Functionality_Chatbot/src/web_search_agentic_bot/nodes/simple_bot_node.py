from src.web_search_agentic_bot.states.simple_state import SimpleState

class SimpleBotNode:

    def __init__(self, model):
        self.model = model

    def get_simple_bot_node(self, state:SimpleState):
        model_response = self.model.invoke(state['messages'])
        return {'messages': [model_response]}
           