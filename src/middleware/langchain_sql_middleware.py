# middleware/olangchain_sql_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from db.postgre_conector import postgres_data_manager

from utils.utils import *
from prompt.prompt import *


class LangChainSQLMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:

            llm = request.state.llm
            
            # Obtém a conexão com o banco e extrai o engine
            engine = postgres_data_manager.get_engine()

            # Cria o objeto SQLDatabase utilizando o engine
            db = SQLDatabase(engine=engine)
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            tools = toolkit.get_tools()

            def get_schema():
                schema = db.get_table_info()
                return schema
            
            def run_query(query):
                return db.run(query['query'].content)

            run_config = RunnablePassthrough.assign(schema=lambda _: get_schema()).assign(question=extract_question)
            template = ChatPromptTemplate.from_template(prompt_sql)
            model_tools = llm.bind_tools(tools, tool_choice="required")

            sql_chain = (
            run_config
            |template 
            |model_tools
            |return_response_sql
            )

            run_config_response = RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: get_schema(),
            response=lambda vars: run_query(vars),)

            template_response = ChatPromptTemplate.from_template(prompt_translate)
            full_chain = (
                run_config_response
                |template_response
                |model_tools
                |return_ia_response
            )

            request.state.sql_chain = sql_chain
            request.state.response_chain = full_chain

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inicializar o agente SQL: {str(e)}")
        
        response = await call_next(request)
        return response
