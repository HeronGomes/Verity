from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import AIMessage
from pydantic import BaseModel
from typing import Optional

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class ModelResponse(BaseModel):
    message: Optional[str] = None  # Mensagem opcional para o sucesso
    error: Optional[str] = None    # Mensagem opcional para o erro

def extract_question(input_data: dict):
    messages = input_data["messages"]
    content = messages[0].content
    return content

def return_response_sql(input_data: AIMessage):
    return input_data

def return_ia_response(messages) -> dict:
    """Submit the final answer to the user based on the query results."""
    return {
        "messages": messages,  # Extrai o SQL como string
    }

