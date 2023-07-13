import ast
from typing import Optional

from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import LLM


def sql_chain(input: str, llm: Optional[LLM] = None):
    db_path = "db/formula1.sqlite"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)

    _llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True) if llm is None else llm  # type: ignore

    db_chain = SQLDatabaseChain.from_llm(
        _llm, db, verbose=True, return_intermediate_steps=True
    )

    result = db_chain(input)

    sql_query = result["intermediate_steps"][1]
    sql_results = ast.literal_eval(result["intermediate_steps"][3])
    answer = result["intermediate_steps"][5]

    return answer, sql_query, sql_results
