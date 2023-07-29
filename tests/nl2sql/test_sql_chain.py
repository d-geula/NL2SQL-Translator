from unittest.mock import patch

import pytest
from langchain.llms.fake import FakeListLLM


@pytest.fixture
def llm():
    response = [
        'SELECT "forename", "surname" FROM drivers WHERE "nationality" = \'Swedish\' LIMIT 5;',
        "Stefan Johansson, Slim Borgudd, Ronnie Peterson, Gunnar Nilsson, Conny Andersson",
    ]
    return FakeListLLM(responses=response)


def test_sql_chain(llm):
    from nl2sql.sql_chain import sql_chain

    with patch("nl2sql.sql_chain._create_llm", return_value=llm):
        answer, sql_query, sql_results = sql_chain("Who are the Swedish drivers?")

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
