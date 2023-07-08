import sqlite3
from contextlib import closing

import pandas as pd

df = pd.read_csv("db/drivers.csv")

# Replace '\N' values with NaN (null) values
df.replace("\\N", pd.NA, inplace=True)

# Define the column types for the table
dtypes = {
    "driverId": "INTEGER PRIMARY KEY",
    "driverRef": "TEXT",
    "number": "INTEGER",
    "code": "TEXT",
    "forename": "TEXT",
    "surname": "TEXT",
    "dob": "TEXT",
    "nationality": "TEXT",
    "url": "TEXT",
}

with closing(sqlite3.connect("db/formula1.sqlite")) as conn:
    df.to_sql("drivers", conn, index=False, if_exists="replace", dtype=dtypes)
