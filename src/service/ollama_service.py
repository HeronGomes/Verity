#service/ollama_service.py
from fastapi import Request
from exception.exceptions import llm_exception
class OllamaService:

    @staticmethod
    def exec_llm(request: Request, question: str):
        try:
            llm = request.state.chat_llm
            result = llm.invoke(question)

            return result
        except Exception as e:
            raise llm_exception("ollama_service - exec_llm - erro: {}".format(e),500)
