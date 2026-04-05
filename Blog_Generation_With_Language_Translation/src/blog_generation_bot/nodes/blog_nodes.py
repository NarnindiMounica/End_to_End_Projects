from src.blog_generation_bot.states.blog_state import BlogState, Blog
from langchain_core.prompts import ChatPromptTemplate

class BlogNodes:

    def __init__(self, llm):
        self.llm = llm

        
    def title_creation_node(self, state:BlogState):
        if "topic" in state or state['topic']:

            system_prompt = """
                            You are an expert in blog creation.
                            Give a suitable title for the given topic in Markdown format.
                            The title should be creative and SEO friendly.
                            Topic: {topic}"""
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt)
            ])

            response = self.llm.invoke(prompt.format(topic=state['topic']))

            return {'blog':{'title': response.content}}


    def content_generation_node(self, state:BlogState):

        system_prompt = """
                        You are an expert in blog creation.
                        For a given title of the topic write a detailed content in Markdown format with bullet points.
                        The content should be in simple text and easy to understand.
                        title: {title}"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])

        response = self.llm.invoke(prompt.format(title=state['blog']['title']))

        return {'blog':{'content': response.content}}
    
    def language_translation_node(self, state:BlogState):

        system_prompt = """
                        You are a multiligual specialist.
                        Translate the given content in desired language without changing the intent and tone of the content.
                        Maintain the same format as given in original content.
                        content: {content}
                        language: {language}
                        """
        
        prompt = ChatPromptTemplate.from_messages(
            [
            ("system", system_prompt),
        ])

        response = self.llm.with_structured_output(Blog).invoke(prompt.format(content=state['blog']['content'],
                                                                              language=state['current_language']))
        
        return {"blog":{"content": response.content}}
    

    def route_decision_maker(self, state:BlogState):

        return state['current_language']

        