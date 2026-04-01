from typing_extensions import TypedDict
from typing import List, Annotated
from langgraph.graph import add_messages

class SimpleState:
    messages : Annotated[List, add_messages]