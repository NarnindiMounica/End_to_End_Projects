from src.web_search_agentic_bot.states.simple_state import SimpleState
from src.web_search_agentic_bot.nodes.simple_bot_node import SimpleBotNode
from src.web_search_agentic_bot.tools.web_search_tools import ToolsNode

from langgraph.prebuilt import tools_condition
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
    
    def web_search_graph_design(self):
        bot_obj = SimpleBotNode(self.model)
        tool_obj = ToolsNode()

        #adding node
        self.graph.add_node("get_simple_bot_node", bot_obj.get_simple_bot_node)
        self.graph.add_node("tools", tool_obj.get_tool_node)

        #adding edges
        self.graph.add_edge(START, "get_simple_bot_node")
        self.graph.add_conditional_edges("get_simple_bot_node", tools_condition)
        self.graph.add_edge("tools", "get_simple_bot_node")
        self.graph.add_edge("get_simple_bot_node", END)

        return self.graph

    def get_usecase_graph(self, usecase):

        if usecase=="Generic Search":
            graph = self.base_graph_design()
            graph_builder = graph.compile()
            return graph_builder
        
        elif usecase=="Web Search":
            graph = self.web_search_graph_design()
            graph_builder = graph.compile()
            return graph_builder



