import sqlite3
from contextlib import closing

import pandas as pd
from sqlparse import format


def execute_query(sql_query: str, db_path: str) -> pd.DataFrame:
    with closing(sqlite3.connect(db_path)) as conn:
        return pd.read_sql_query(sql_query, conn)


def format_query(sql: str) -> str:
    try:
        formatted_sql_query = format(sql, reindent=True, keyword_case="upper")
        markdown_code_block = f"```\n{formatted_sql_query}\n```"
        return markdown_code_block
    except Exception as e:
        print(f"An error occurred while formatting the SQL query: {e}")
        return sql
