from typing_extensions import TypedDict

class Blog(TypedDict):
    title:str
    content:str

class BlogState(TypedDict):
    topic:str
    blog:Blog 
    current_language:str   