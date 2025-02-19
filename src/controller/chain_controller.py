# controller/chain_controller.py

from fastapi import HTTPException, Request
from service.lang_chain_service import LangChainService

class ChainController:
    @staticmethod
    def process_chain(request: Request, question: str):
        # Validação simples da entrada
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

        try:
            # Chama o serviço para processar a pergunta
            result = LangChainService(request).process_chain(question)
            return result
        except HTTPException as http_exc:
            # Relevanta exceções HTTP personalizadas do serviço diretamente
            raise http_exc
        except Exception as e:
            # Exceções genéricas: retornar um erro detalhado com status 500
            raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar a pergunta: {str(e)}")