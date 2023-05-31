# import os
import sqlite3

import openai
import pandas as pd

# openai.api_key = os.getenv("OPENAI_API_KEY")
# or
# openai.api_key = "####"

def get_openai_response(prompt, agent):
    
    # Load the system message from the agent's file
    with open(f'agents/{agent}.txt', 'r') as file:
        system_message = file.read()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"{system_message}"},
                {"role": "user", "content": f"{prompt}"+"\n#"}
            ]
    )

    return response["choices"][0]["message"]["content"] # type: ignore


def process_query(query):

    conn = sqlite3.connect('files/nba.sqlite')
    # Execute the query and load the results into a pandas dataframe
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df