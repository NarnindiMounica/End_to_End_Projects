from src.web_search_agentic_bot.states.simple_state import SimpleState
from src.web_search_agentic_bot.nodes.simple_bot_node import SimpleBotNode

from langgraph.graph import StateGraph, START, END

class SelectGraph:
    def __init__(self, model):
        self.graph = StateGraph(SimpleState)
        self.model = model
        
    def base_graph_design(self):
        bot_obj = SimpleBotNode(self.model)

        #adding node
        self.graph.add_node("get_simple_bot_node", bot_obj.get_simple_bot_node)

        #adding edges
        self.graph.add_edge(START, "get_simple_bot_node")
        self.graph.add_edge("get_simple_bot_node", END)

        return self.graph

    def get_usecase_graph(self, usecase):

        if usecase=="Generic Search":
            graph = self.base_graph_design(self.model)
            graph_builder = graph.compile()
            return graph_builder



