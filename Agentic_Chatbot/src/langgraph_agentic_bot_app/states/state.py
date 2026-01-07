from typing_extensions import TypedDict
from typing import Annotated, List

from langgraph.graph.message import add_messages

class BotState(TypedDict):
    messages: Annotated[List, add_messages]