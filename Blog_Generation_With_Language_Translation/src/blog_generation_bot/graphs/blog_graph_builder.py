from langgraph.graph import StateGraph, START, END

from src.blog_generation_bot.states.blog_state import BlogState
from src.blog_generation_bot.nodes.blog_nodes import BlogNodes

class BlogGraphBUilder:

    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def get_blog_graph_builder(self):

        blog_nodes_obj = BlogNodes(llm=self.llm)
        #adding nodes

        self.graph.add_node("title_creation_node",blog_nodes_obj.title_creation_node)
        self.graph.add_node("content_generation_node",blog_nodes_obj.content_generation_node)

        #adding edges
        self.graph.add_edge(START, "title_creation_node")
        self.graph.add_edge("title_creation_node", "content_generation_node")
        self.graph.add_edge("content_generation_node", END)

        #graph builder
        graph_builder = self.graph.compile()

        return graph_builder




