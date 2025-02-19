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
        model_name = os.getenv("OLLAMA_MODEL")
        if not model_name:
            raise RuntimeError("Variável de ambiente 'OLLAMA_MODEL' não encontrada.")
        
        # Inicializa o LLM com o modelo
        self.llm = ChatOllama(model=model_name, temperature=0)

    async def dispatch(self, request: Request, call_next):
        try:
            # Atribui o LLM ao estado da requisição
            request.state.llm = self.llm
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inicializar o agente SQL: {str(e)}")
        
        # Continua o fluxo da requisição
        response = await call_next(request)
        return response

