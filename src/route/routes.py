#route/routes.py
from fastapi import APIRouter, Form, Request, HTTPException
from controller.chain_controller import ChainController
from controller.ollama_controller import OllamaController
from fastapi.responses import JSONResponse,HTMLResponse
from utils.utils import ModelResponse
router = APIRouter()


@router.get("/",include_in_schema=False)
async def root():
    html_content = """
    <html>
        <head>
            <title>Welcome</title>
            <style>
                body {
                    font-family: monospace;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 18px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <pre>

VVVVVVVV           VVVVVVVVEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRR  IIIIIIIIII TTTTTTTTTTTTTTTTTTTTTTYYYYYYY         YYYYYYY
V::::::V           V::::::VE::::::::::::::::::::ER::::::::::::::::R  I::::::::IT:::::::::::::::::::::TY:::::Y         Y:::::Y
V::::::V           V::::::VE::::::::::::::::::::ER::::::RRRRRR:::::R I::::::::IT:::::::::::::::::::::TY:::::Y         Y:::::Y
V::::::V           V::::::VEE::::::EEEEEEEEE::::ERR:::::R     R:::::RII::::::IIT:::::TT:::::::TT:::::TTY::::::Y      Y::::::Y
 V:::::V           V:::::V   E:::::E       EEEEEERR::::R     R:::::R   I::::I  TTTTTT  T:::::T  TTTTTTYYY:::::::Y   Y:::::::Y
  V:::::V         V:::::V    E:::::E             R::::R     R:::::R    I::::I          T:::::T         YYY::::::Y Y::::::YYY
   V:::::V       V:::::V     E::::::EEEEEEEEEE   R::::RRRRRR:::::R     I::::I          T:::::T            Y:::::::Y:::::::Y
    V:::::V     V:::::V      E:::::::::::::::E   R:::::::::::::RR      I::::I          T:::::T             Y:::::::::::::Y
     V:::::V   V:::::V       E:::::::::::::::E   R::::RRRRRR:::::R     I::::I          T:::::T              Y:::::::::::Y
      V:::::V V:::::V        E::::::EEEEEEEEEE   R::::R     R:::::R    I::::I          T:::::T               Y:::::::::Y
       V:::::V:::::V         E:::::E             R::::R     R:::::R    I::::I          T:::::T                Y:::::::Y
        V:::::::::V          E:::::E       EEEEEERR::::R     R:::::R   I::::I          T:::::T                Y:::::Y
         V:::::::V         EE::::::EEEEEEEE:::::ERR:::::R     R:::::RII::::::II      TT:::::::TT              Y:::::Y
          V:::::V          E::::::::::::::::::::ER::::::R     R:::::RI::::::::I      T:::::::::T              Y:::::Y
           V:::V           E::::::::::::::::::::ER::::::R     R:::::RI::::::::I      T:::::::::T              Y:::::Y
            VVV            EEEEEEEEEEEEEEEEEEEEEERRRRRRRR     RRRRRRRIIIIIIIIII      TTTTTTTTTTT              YYYYYYY
   

                </pre>
                <p>Clique no link abaixo para acessar o serviço:</p>
                <a href="/docs">Acessar o serviço</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.post("/ollama_ask",tags=['DEBUG'])
async def ollama_ask(request: Request, question: str = Form(...)):
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
            content=ModelResponse(message=result['sql_content']).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(message="Um erro ocorreu, tente novamente mais tarde",error=f"Erro inesperado: {str(e)}").dict()
        )



@router.post("/ask")
async def ask(request: Request, question: str = Form(...)):
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
        result = ChainController.process_chain(request, question)
        
        return JSONResponse(
            status_code=200,
            content=ModelResponse(message=result['sql_content']).dict()
        )

    except Exception as e:
        # Captura qualquer outro erro e retorna um erro interno
        return JSONResponse(
            status_code=500,
            content=ModelResponse(message="Um erro ocorreu, tente novamente mais tarde",error=f"Erro inesperado: {str(e)}").dict()
        )