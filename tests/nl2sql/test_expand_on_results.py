def test_expand_on_results():
    from nl2sql.expand_on_results import expand_on_results
    from tests.utils.assert_summary_using_qa import assert_summary_using_qa

    summary = expand_on_results(
        docs="docs/martin_brundle.txt",
        user_query="Tell me about Martin Brundle",
        sql_results=[('Martin', 'Brundle', '1959-06-01', 'British')],
    )

    assert_summary_using_qa(
        summary=summary,
        questions_and_answers = {
            "Who is this summary about?": "Martin Brundle",
            "Are they known for being a commentator?": "Yes",
            "Are they known for being a driver?": "Yes",
        })
