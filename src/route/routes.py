from fastapi import APIRouter, Form, Request, HTTPException, Body
from controller.ollama_controller import OllamaController
from controller.chain_controller import ChainController
from fastapi.responses import JSONResponse
from utils.utils import ModelResponse
router = APIRouter()

@router.post("/process_question",tags=['DEBUG'])
async def process_question(request: Request, question: str = Form(...)):
    """
    Rota que recebe uma pergunta em linguagem natural e utiliza o controller
    para convertê-la em uma consulta processada por um LLM.
    
    Parâmetros:
    - question: A pergunta em linguagem natural que será convertida.
    
    Retorna:
    - O resultado processado pelo LLM, no formato JSON.
    """
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        # Chama o controlador de forma assíncrona
        result = OllamaController.process_question(request, question)
        
        return JSONResponse(
            status_code=200,
            content=ModelResponse(message=result).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(error=f"Erro inesperado: {str(e)}").dict()
        )


@router.post("/chain_human2sql",tags=['DEBUG'])
async def chain_human2sql(request: Request, question: str = Form(...)):
    """
    Rota que recebe uma pergunta em linguagem natural e utiliza o controller
    para convertê-la em uma consulta processada por um LLM.
    
    Parâmetros:
    - question: A pergunta em linguagem natural que será convertida.
    
    Retorna:
    - O resultado processado pelo LLM, no formato JSON.
    """
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        # Chama o controlador de forma assíncrona
        result = ChainController.process_chain_question2sql(request, question)
        
        return JSONResponse(
            status_code=200,
            content=ModelResponse(message=result).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(error=f"Erro inesperado: {str(e)}").dict()
        )
    

@router.post("/chain_sql2response",tags=['DEBUG'])
async def chain_sql2response(request: Request, question: str = Form(...)):
    """
    Rota que recebe uma pergunta em linguagem natural e utiliza o controller
    para convertê-la em uma consulta processada por um LLM.
    
    Parâmetros:
    - question: A pergunta em linguagem natural que será convertida.
    
    Retorna:
    - O resultado processado pelo LLM, no formato JSON.
    """
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        # Chama o controlador de forma assíncrona
        result = ChainController.process_chain_sql2response(request, question)
        return JSONResponse(
            status_code=200,
            content=ModelResponse(message=result).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(error=f"Erro inesperado: {str(e)}").dict()
        )

@router.post("/chain_full",tags=['DEBUG'])
async def chain_full(request: Request, question: str = Form(...)):
    """
    Rota que recebe uma pergunta em linguagem natural e utiliza o controller
    para convertê-la em uma consulta processada por um LLM.
    
    Parâmetros:
    - question: A pergunta em linguagem natural que será convertida.
    
    Retorna:
    - O resultado processado pelo LLM, no formato JSON.
    """
    if not question or question.strip() == "":
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        # Chama o controlador de forma assíncrona
        result = ChainController.process_chain_full(request, question)
        return JSONResponse(
            status_code=200,
            content=ModelResponse(message=result).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(error=f"Erro inesperado: {str(e)}").dict()
        )