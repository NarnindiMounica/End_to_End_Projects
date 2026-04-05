from langgraph.graph import StateGraph, START, END

from src.blog_generation_bot.states.blog_state import BlogState
from src.blog_generation_bot.nodes.blog_nodes import BlogNodes

class BlogGraphBuilder:

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

        return self.graph
    
    def get_setup_graph(self, usecase):

        if usecase=="topic":
            return self.get_blog_graph_builder().compile()
        

#below code is for langgraph studio

from src.blog_generation_bot.llms.groq_model import GroqModel

llm = GroqModel().get_groq_model()
graph_builder = BlogGraphBuilder(llm=llm)
blog_agent = graph_builder.get_blog_graph_builder().compile()




