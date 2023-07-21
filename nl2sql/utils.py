from sqlparse import format, parse, sql
from sqlparse.tokens import Wildcard


def extract_columns(query):
    """Extracts the selected columns from a SQL query"""
    parsed = parse(query)[0]
    print(parsed)
    select_items = []

    for token in parsed.tokens:
        if (
            isinstance(token, sql.Identifier)
            or isinstance(token, sql.IdentifierList)
            or isinstance(token, sql.Function)
            or token.ttype is Wildcard
        ):
            select_items = str(token).split(", ")
            break

    for i, item in enumerate(select_items):
        if " AS " in item:
            select_items[i] = item.split(" AS ")[1]

    return None if all(item == "*" for item in select_items) else select_items


def format_query(sql):
    """Formats a SQL query and returns it as a markdown code block"""
    beautified =  format(sql, reindent=True, keyword_case="upper")

    return f"```\n{beautified}\n```"