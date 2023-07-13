import pytest


TEST_QUERIES = [
    "SELECT name, age FROM users;",
    "SELECT * FROM orders;",
    "SELECT COUNT(*) FROM products;",
    "SELECT AVG(price), MAX(price), MIN(price) FROM sales;",
    "SELECT name, age, COUNT(*) FROM users GROUP BY name, age;",
    "SELECT * FROM orders WHERE date >= '2021-01-01' AND date <= '2021-12-31';",
    "SELECT AVG(price), MAX(price), MIN(price) FROM sales WHERE date >= '2021-01-01' AND date <= '2021-12-31';",
    "SELECT name, age, COUNT(*) FROM users WHERE age >= 18 GROUP BY name, age HAVING COUNT(*) > 1;",
    "SELECT name AS full_name, age FROM users;",
    "SELECT u.name AS full_name, COUNT(o.id) AS num_orders FROM users AS u JOIN orders AS o ON u.id = o.user_id WHERE o.date >= '2021-01-01' GROUP BY u.name HAVING COUNT(o.id) > 1;",
    "SELECT my_table.* FROM my_table;",
]

EXPECTED_COLUMNS = [
    ['name', 'age'],
    ['*'],
    ['COUNT(*)'],
    ['AVG(price)', 'MAX(price)', 'MIN(price)'],
    ['name', 'age', 'COUNT(*)'],
    ['*'],
    ['AVG(price)', 'MAX(price)', 'MIN(price)'],
    ['name', 'age', 'COUNT(*)'],
    ['full_name', 'age'],
    ['full_name', 'num_orders'],
    ['my_table.*']
]

@pytest.mark.parametrize("query, expected_columns", zip(TEST_QUERIES, EXPECTED_COLUMNS))
def test_extract_columns(query, expected_columns):
    from nl2sql.utils import extract_columns
    assert extract_columns(query) == expected_columns