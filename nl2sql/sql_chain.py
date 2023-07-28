import ast

from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI


def sql_chain(input: str):
    db_path = "db/formula1.sqlite"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)

    db_chain = SQLDatabaseChain.from_llm(
        _create_llm(), db, verbose=True, return_intermediate_steps=True
    )

    result = db_chain(input)

    sql_query = result["intermediate_steps"][1]
    sql_results = ast.literal_eval(result["intermediate_steps"][3])
    answer = result["intermediate_steps"][5]

    return answer, sql_query, sql_results

def _create_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True) # type: ignore