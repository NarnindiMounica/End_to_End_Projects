from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

class ToolsNode:

    def __init__(self, user_controls):
        self.user_controls = user_controls

    def get_bind_tools(self):

        tavily_tool = TavilySearch(max_serach=5, topic="general", search_depth="basic")
        tools=[tavily_tool]
        return tools
    
    def get_tool_node(self):
        return ToolNode(self.get_bind_tools())

