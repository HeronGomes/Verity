# middleware/olangchain_sql_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import ChatPromptTemplate
from db.postgre_conector import postgres_data_manager
from langgraph.graph import END, StateGraph, START
from utils.utils import *
from prompt.prompt import *

class LangChainSQLMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:

            engine = postgres_data_manager.get_engine()
            db = SQLDatabase(engine)
            llm_chat = request.state.chat_llm
            llm_fix_sql = request.state.fix_sql_llm
            toolkit = SQLDatabaseToolkit(db=db, llm=llm_chat)
            tools = toolkit.get_tools()
            model_tools = llm_chat.bind_tools(tools, tool_choice="required")

            agent_sql_fixer = llm_fix_sql
            agent_sql_fixer_tools = agent_sql_fixer.bind_tools(tools,tool_choice="required")

            def get_schema():
                schema = db.get_table_info()
                return schema

            def run_query(query : str):
                try:
                    return db.run(query)
                except Exception as err:
                    raise Exception(err)
                            
                        
            def natural_language2sql(state:State):
                template_question = ChatPromptTemplate.from_template(natural_language2sql_prompt.format(schema=get_schema(),question=state['question']))
                response = self.model_tools.invoke(template_question.format_prompt())
                state['sql'] = response.content
                return state

            def sql2natural_language(state:State):
                template_response = ChatPromptTemplate.from_template(sql2natural_language_prompt.format(schema=get_schema(),query=state['sql'],response=state['sql_content'],question=state['question']))
                response = self.model_tools.invoke(template_response.format_prompt())
                state['sql_content'] = response.content
                return state
                        
            def sql_fix(bad_sql:str):
                template_response = ChatPromptTemplate.from_template(sql_agent_fixer_prompt.format(schema=get_schema(),query=bad_sql))
                response = self.agent_sql_fixer_tools.invoke(template_response.format_prompt())
                return response

            
            def check_sql(state: State):    
                if state['erro']:
                    return 'FAIL'
                return 'PASS'

            def execute_sql(state: State):
                query = state['sql']
                try:
                    state['sql_content'] = run_query(query)
                    state['erro'] = False
                except Exception as err:
                    state['erro'] = True
                    
                return state

            def melhore_sql(state:State):
                try:
                    msg = sql_fix(state['sql'])
                    state['sql'] = msg.content
                    state = execute_sql(state)
                    state['erro'] = False
                except Exception as err:
                    state['erro'] = True

            self.model_tools = model_tools
            self.agent_sql_fixer_tools = agent_sql_fixer_tools

            app = self.make_graph(natural_language2sql, sql2natural_language, check_sql, execute_sql, melhore_sql)

            request.state.chain = app
           
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao inicializar o agente SQL: {str(e)}")
        
        response = await call_next(request)
        return response

    def make_graph(self, natural_language2sql, sql2natural_language, check_sql, execute_sql, melhore_sql):
        workflow = StateGraph(State)
            # Add nodes
        workflow.add_node("language2sql", natural_language2sql)
        workflow.add_node("melhore_sql", melhore_sql)
        workflow.add_node("execute_sql", execute_sql)
        workflow.add_node("sql2response", sql2natural_language)

            # Add edges to connect nodes
        workflow.add_edge(START, "language2sql")
        workflow.add_edge("language2sql", "melhore_sql")
        workflow.add_edge("melhore_sql", "execute_sql")
        workflow.add_conditional_edges(
                "execute_sql", check_sql, {'FAIL':'melhore_sql','PASS':'sql2response'}
            )

        workflow.add_edge("melhore_sql","execute_sql")


        workflow.add_edge("sql2response",END)

            # Compile
        app = workflow.compile()
        return app
