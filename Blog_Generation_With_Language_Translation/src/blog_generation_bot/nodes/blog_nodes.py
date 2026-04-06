from src.blog_generation_bot.states.blog_state import BlogState, Blog
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

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

        return {'blog':{'title': state['blog']['title'], 'content': response.content}}
    
    def language_translation_node(self, state:BlogState):

        translational_prompt = """
                        Translate the following content into {current_language} language.
                        - Maintain original tone, style and formatting.
                        - Adapt cultural references and idioms to be suitable for {current_language} language.
                        - Return the result strictly in two fields "title" and "content".
                        - Keep the content of around 1000 words.
                        original content: {blog_content}
                        """
        blog_content= state['blog']['content']
        messages=[
            HumanMessage(translational_prompt.format(blog_content=blog_content, current_language=state['current_language']))
        ]
       
        response = self.llm.with_structured_output(Blog).invoke(messages)
        
        return {"topic": state['topic'], "blog":{"title":response['title'], "content": response['content']}, "current_language": state['current_language']
    

    def language_router(self, state:BlogState):

        return {"current_language": state['current_language']}
    
    def route_decision_maker(self, state:BlogState):

        if state['current_language']=="hindi":
            return "hindi"
        elif state['current_language']=="telugu":
            return "telugu"
        


        