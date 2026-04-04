from src.blog_generation_bot.states.blog_state import BlogState
from langchain_core.prompts import ChatPromptTemplate

class BlogNodes:

    def __init__(self, llm):
        self.llm = llm
        self.state=BlogState
        
    def title_creation_node(self, BlogState):

        system_prompt = """
                        You are an expert in blog creation.
                        Give a suitable title for the given topic in Markdown format.
                        The title should be creative and SEO friendly.
                        Topic: {topic}"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])

        response = self.llm.invoke(prompt.format(topic=self.state.topic))

        return {self.state.blog['title']: response.content}


    def content_generation_node(self, BlogState):

        system_prompt = """
                        You are an expert in blog creation.
                        For a given title of the topic write a detailed content in Markdown format with bullet points.
                        The content should be in simple text and easy to understand.
                        title: {title}"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])

        response = self.llm.invoke(prompt.format(title=self.state.blog['title']))

        return {self.state.blog['content']: response.content}

        