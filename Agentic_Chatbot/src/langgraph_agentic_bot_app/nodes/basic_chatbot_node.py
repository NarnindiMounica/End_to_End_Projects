from src.langgraph_agentic_bot_app.states.state import BotState


class BasicBotNode:
    def __init__(self,model):
        self.llm = model

    def basic_chatbot(self, state:BotState):
        "this method takes user_message and invokes model for response"
        bot_model = self.llm
        msg=state['messages']
        response = bot_model.invoke(msg)  
        return {"messages": [response]}  

