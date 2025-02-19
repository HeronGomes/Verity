# service/lang_chain_service.py
from fastapi import Request
from utils.utils import *
from dotenv import load_dotenv
from os import getenv
load_dotenv()

class LangChainService:
    def __init__(self,request : Request):
        self.chain = request.state.chain

    def process_chain(self,question: str):
        try:
            # Usa o agente SQL para transformar a pergunta em consulta e executá-la
            param_question = {"question":question}
            return self.chain.invoke(param_question,{"recursion_limit": int(getenv('RECURSION_LIMIT'))})
        except Exception as err:
            raise Exception("query_service - process_chain - erro: {}".format(err))
