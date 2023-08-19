from unittest.mock import patch

import pandas as pd
import pytest
from langchain.llms.fake import FakeListLLM
from pandas.testing import assert_frame_equal


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
        sql_query, sql_results = sql_chain("Who are the Swedish drivers?")

        assert (
            sql_query
            == 'SELECT "forename", "surname" FROM drivers WHERE "nationality" = \'Swedish\' LIMIT 5;'
        )

        expected_results = pd.DataFrame({
            "forename": ["Stefan", "Slim", "Ronnie", "Gunnar", "Conny"],
            "surname": ["Johansson", "Borgudd", "Peterson", "Nilsson", "Andersson"]
        })
        assert_frame_equal(sql_results, expected_results)
