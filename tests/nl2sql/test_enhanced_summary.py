import ast
from pathlib import Path


def test_enhanced_summary():
    from nl2sql.enhanced_summary import enhanced_summary
    from tests.utils.summary_category_extractor import \
        summary_category_extractor

    summary = enhanced_summary(
        docs=Path("docs/martin_brundle.txt").read_text(),
        user_query="Tell me about Martin Brundle",
        sql_results=[('Martin', 'Brundle', '1959-06-01', 'British')],
    )

    categories = ast.literal_eval(summary_category_extractor(
        summary=summary,
        question_1="Who is this summary about?",
        question_2="Did they win a formula 1 championship?",
        # question_3="Are they married with children?"
        ))
    
    assert categories["Who is this summary about?"] == ["Martin Brundle"]
    assert categories["Did they win a formula 1 championship?"] == ["No"]
    