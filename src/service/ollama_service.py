from fastapi import Request, HTTPException

class OllamaService:

    @staticmethod
    def exec_llm(request: Request, question: str):
        # Verifica se o objeto LLM está presente no request.state
        llm = getattr(request.state, 'llm', None)
        if llm is None:
            raise HTTPException(status_code=500, detail="LLM não está disponível no request. Middleware não configurado corretamente.")

        try:

            # Usa o agente SQL para transformar a pergunta em consulta e executá-la
            result = llm.invoke(question)

            # Retorna o resultado do LLM
            return result
        except Exception as e:
            # Tratamento de erro ao invocar o LLM
            raise HTTPException(status_code=500, detail=f"Erro ao executar o LLM: {str(e)}")
