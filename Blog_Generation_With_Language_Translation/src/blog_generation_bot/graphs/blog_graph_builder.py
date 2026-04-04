from langgraph.graph import StateGraph, START, END

from src.blog_generation_bot.states.blog_state import BlogState

class BlogGraphBUilder:

    def __init__(self):
        self.graph = StateGraph(BlogState)

    def get_blog_graph_builder(self):

        #adding nodes

        self.graph.add_node("title_creation_node",)
        self.graph.add_node("content_generation_node",)

        #adding edges
        self.graph.add_edge(START, "title_creation_node")
        self.graph.add_edge("title_creation_node", "content_generation_node")
        self.graph.add_edge("content_generation_node", END)

        #graph builder
        graph_builder = self.graph.compile()

        return graph_builder




