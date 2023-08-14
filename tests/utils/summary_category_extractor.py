import langchain
from langchain.cache import SQLiteCache
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def summary_category_extractor(summary: str, question_1: str, question_2: str):
    chat = ChatOpenAI(temperature=0.0, verbose=True)  # type: ignore

    langchain.llm_cache = SQLiteCache(database_path="tests/test_cache.db")

    system_template = """
    This function extracts categories from a generated summary based on the questions provided.

    Args:
	    summary (str): The generated summary.
        questions (list): A list of questions.

    Returns:
	    dict: A dictionary of extracted categories. Keys may have multiple values. 
              Values represent single word categories where possible.
              
    Example:
        The returned dictionary may look something like this:

            "Question1": ["Value1", "Value2"],
            "Question2": ["Value3"],
            ..."""

    human_template = """
    summary: {summary}
    qestions: ["{q1}", "{q2}"]"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    return chat(
        chat_prompt.format_prompt(
            summary=summary, q1=question_1, q2=question_2
        ).to_messages()
    ).content