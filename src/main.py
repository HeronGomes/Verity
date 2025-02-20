#main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from middleware.langchain_sql_middleware import LangChainSQLMiddleware
from middleware.ollama_middleware import OllamaMiddleware
from route.routes import router as query_router
import subprocess

def get_git_version():
    '''
        Obtem a versão da API baseada no commit, se ocorrer padrão de tags, retorna o valor.
    '''
    try:
        version = subprocess.check_output(["git", "describe", "--tags", "--always"]).strip().decode('utf-8')
        return version
    except Exception as e:
        return "1.0.0"


# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="Verity API",
    description="API desenvolvida com motor de gen a.i capaz de interpretar sql a partir de linguagem natural.",
    version=get_git_version()
)

# Middleware de CORS para permitir requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Defina origens específicas em produção
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

# Registra o middleware LangChainSQLMiddleware que injeta o agente SQL
app.add_middleware(LangChainSQLMiddleware)

# Registra o middleware OllamaMiddleware que injeta o LLM
app.add_middleware(OllamaMiddleware)

# Inclui as rotas com um prefixo definido para a API
app.include_router(query_router, prefix='/verity')

# Mensagem de inicialização
@app.on_event("startup")
async def startup_event():
    print("API Verity está rodando!")

# Mensagem de desligamento
@app.on_event("shutdown")
async def shutdown_event():
    print("API Verity foi desligada.")
