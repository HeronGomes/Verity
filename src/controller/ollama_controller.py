# controller/ollama_controller.py

from fastapi import HTTPException, Request
from service.ollama_service import OllamaService

class OllamaController:
    @staticmethod
    def process_question(request: Request, question: str):
        # Validação simples da entrada
        if not question or question.strip() == "":
            raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

        try:
            # Chama o serviço para processar a pergunta
            result = OllamaService.exec_llm(request, question)
            return result.content
        except HTTPException as http_exc:
            # Relevanta exceções HTTP personalizadas do serviço diretamente
            raise http_exc
        except Exception as e:
            # Exceções genéricas: retornar um erro detalhado com status 500
            raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar a pergunta: {str(e)}")

