from src.web_search_agentic_bot.states.simple_state import SimpleState

class SimpleBotNode:

    def __init__(self, state, model):
        self.state = state
        self.model = model

    def get_simple_bot_node(self):
        model_response = self.model.invoke(self.state['messages'])
        return {self.state['messages']: model_response}
           