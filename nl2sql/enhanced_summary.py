import langchain
from langchain.cache import SQLiteCache
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def enhanced_summary(docs: str, user_query: str, sql_results: list):
    chat = ChatOpenAI(temperature=0.0, verbose=True)  # type: ignore

    langchain.llm_cache = SQLiteCache(database_path="cache/.langchain.db")

    template = """
    Given a user query and a table of results, use the extra context \
    provided to create a concise, rich summary of the query and the \
    results - the extra context is supplemental to the query and results:
        
    Extra context: {docs}"""

    human_template = """
    User query: {user_query}
    SQL results: {sql_results}"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    return chat(
        chat_prompt.format_prompt(
            docs=docs, user_query=user_query, sql_results=sql_results
        ).to_messages()
    ).content
