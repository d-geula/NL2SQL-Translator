from pandas.testing import assert_frame_equal


def assert_frame_ignore_order(sql_results, expected_results):
    sql_results = sql_results.sort_values(["forename", "surname"]).reset_index(drop=True)
    expected_results = expected_results.sort_values(["forename", "surname"]).reset_index(drop=True)

    return assert_frame_equal(sql_results, expected_results)