# service/query_service.py
from fastapi import Request
from langgraph.graph import END, StateGraph, START
from utils.utils import *
from langchain_core.messages import AIMessage,HumanMessage

class LangChainService:
    def __init__(self,request : Request):
        self.sql_chain = request.state.sql_chain
        self.response_chain = request.state.response_chain

        self.lang_chain = self.make_graph()

    def process_chain_question2sql(self,question: str):
        # Usa o agente SQL para transformar a pergunta em consulta e executá-la
        param_question = {"messages":[HumanMessage(content=question)]}
        return self.sql_chain.invoke(param_question)
    
    def process_chain_sql2response(self,question: str):
        # Usa o agente SQL para transformar a pergunta em consulta e executá-la
        param_question = {"messages":[AIMessage(content=question)]}
        return self.response_chain.invoke(param_question)

    def process_chain_full(self,question: str):
        # Usa o agente SQL para transformar a pergunta em consulta e executá-la
        param_question = {"messages":[HumanMessage(content=question)]}
        return self.lang_chain.invoke(param_question)

    def make_graph(self):
        workflow = StateGraph(State)
        workflow.add_node("make_sql_node", self.sql_chain)
        workflow.add_node("make_response_node", self.response_chain)

        workflow.add_edge(START, "make_sql_node")
        workflow.add_conditional_edges("make_sql_node", should_continue,['make_response_node',END])
        workflow.add_edge("make_response_node",END)

        app = workflow.compile()

        return app

def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.content.upper().startswith('ERRO'):
        return "make_sql_node"
    else:
        return 'make_response_node'

