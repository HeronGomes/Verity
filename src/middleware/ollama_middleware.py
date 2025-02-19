from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

class OllamaMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Carrega o modelo apenas uma vez para melhorar a eficiência
        chat_model = os.getenv("CHAT_OLLAMA_MODEL")
        if not chat_model:
            raise RuntimeError("Variável de ambiente 'OLLAMA_MODEL' não encontrada.")
        
        fix_sql_model = os.getenv("SQL_FIX_OLLAMA_MODEL")
        if not fix_sql_model:
            raise RuntimeError("Variável de ambiente 'SQL_FIX_OLLAMA_MODEL' não encontrada.")
        
        # Inicializa o LLM com o modelo
        self.chat_llm = ChatOllama(model=chat_model, temperature=0.5)
        self.fix_sql_llm = ChatOllama(model=fix_sql_model, temperature=0)

    async def dispatch(self, request: Request, call_next):
        try:
            # Atribui o LLM ao estado da requisição
            request.state.chat_llm = self.chat_llm
            request.state.fix_sql_llm = self.fix_sql_llm
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inicializar o agente SQL: {str(e)}")
        
        # Continua o fluxo da requisição
        response = await call_next(request)
        return response

