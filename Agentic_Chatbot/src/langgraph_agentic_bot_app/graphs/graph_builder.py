from langgraph.graph import StateGraph, START, END

from src.langgraph_agentic_bot_app.states.state import BotState
from src.langgraph_agentic_bot_app.nodes.basic_chatbot_node import BasicBotNode


class GraphSelector:
    def __init__(self, model):
        self.llm = model

    def get_graph_builder(self):

        """
        Docstring for get_graph_builder
        
        this method has the graph workflow for basic chatbot usecase
        """
        self.graph_builder = StateGraph(BotState)

        self.botnode_obj = BasicBotNode(self.llm)

        self.graph_builder.add_node("basicchatbotnode",self.botnode_obj.basic_chatbot)

        self.graph_builder.add_edge(START, "basicchatbotnode")
        self.graph_builder.add_edge("basicchatbotnode", END)

        return self.graph_builder
    
    def select_graph(self, usecase):
        """
        Docstring for select_graph_builder
        :param usecase: provide the usecase to select suitable graph_builder

        This method provides compiled graph based on usecase provided.

        """
        if usecase.lower()=="basic chatbot":
            self.selected_builder = self.get_graph_builder()
            graph = self.selected_builder.compile()
            return graph


