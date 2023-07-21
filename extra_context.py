from pathlib import Path
from nl2sql.enahnced_summary import enhanced_summary

docs = Path("docs/martin_brundle.txt").read_text()
user_query, sql_results = ("Tell me about Martin Brundle", [("Martin", "Brundle", "1959-06-01", "British")])

print(enhanced_summary(docs, user_query, sql_results))