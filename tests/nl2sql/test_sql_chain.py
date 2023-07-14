import pytest
from langchain.llms.fake import FakeListLLM


@pytest.fixture
def llm():
    response = [
        'SELECT "forename", "surname" FROM drivers WHERE "nationality" = \'Swedish\' LIMIT 5;',
        "Stefan Johansson, Slim Borgudd, Ronnie Peterson, Gunnar Nilsson, Conny Andersson",
    ]
    llm = FakeListLLM(responses=response)

    return llm


def test_nl_to_sql(llm):
    from nl2sql.sql_chain import sql_chain

    answer, sql_query, sql_results = sql_chain(
        "What are the names of the Swedish drivers?", llm
    )

    assert (
        answer
        == "Stefan Johansson, Slim Borgudd, Ronnie Peterson, Gunnar Nilsson, Conny Andersson"
    )
    assert (
        sql_query
        == 'SELECT "forename", "surname" FROM drivers WHERE "nationality" = \'Swedish\' LIMIT 5;'
    )
    assert sql_results == [
        ("Stefan", "Johansson"),
        ("Slim", "Borgudd"),
        ("Ronnie", "Peterson"),
        ("Gunnar", "Nilsson"),
        ("Conny", "Andersson"),
    ]
