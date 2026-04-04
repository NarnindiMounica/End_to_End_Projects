from typing_extensions import TypedDict
from pydantic import BaseModel

class Blog(TypedDict):
    title:str
    content:str

class BlogState(BaseModel):
    topic:str
    blog:Blog 
    current_language:str   