from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

class ToolsNode:

    def get_bind_tools(self):

        tavily_tool = TavilySearch(max_search=2, topic="general", search_depth="basic")
        tools=[tavily_tool,]
        return tools
    

