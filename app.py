from pathlib import Path

import gradio as gr

import utils

# Define some example queries
examples = [
    ["How many players are there with a first name that begins with 'John'?"],
    ["Is steph curry active?"],
    ["List all players with a last name of Jordan"],
]

# Main function
def nl_to_sql(prompt):
    
    # Translate the natural language query to SQL using the OpenAI API
    sql_query = utils.get_openai_response(prompt, "sql_agent")

    # Process the SQL query
    query_result = utils.process_query(sql_query)

    # Describe the results of the query using the OpenAI API
    query_description = utils.get_openai_response(
        f'Question: {prompt}\nSQL Query: {sql_query}\nQuery Result: {query_result}', 
        "descriptor_agent"
    )

    return query_description, sql_query, query_result


""" gr.Interface method example
app = gr.Interface(
    nl_to_sql,
    inputs=gr.Textbox(placeholder="What would you like to know?", lines=1, label="Question:"),
    outputs=[gr.Textbox(lines=1, label="Data summary:"), gr.DataFrame(label="Data:")],
    examples=examples,
) """

callback = gr.CSVLogger() # See docs: https://gradio.app/using-flagging/#flagging-with-blocks

with gr.Blocks() as app:

    gr.Markdown(Path('description.md').read_text())

    with gr.Row():
        with gr.Column(scale=2):
            inp = gr.Textbox(placeholder="What would you like to know?", lines=1, label="Question:")
            with gr.Row():
                btn_run = gr.Button("Execute query")
                btn_flag = gr.Button("Flag", variant="stop")
            gr.Examples(examples, inp)

        with gr.Column(scale=3):
            summ_out = gr.Textbox(lines=1, label="Data summary:")
            sql_out = gr.Textbox(lines=1, label="SQL query:")
            df_out = gr.DataFrame()

    callback.setup([inp, summ_out, sql_out, df_out], "flagged_data_points")

    btn_run.click(fn=nl_to_sql, inputs=inp, outputs=[summ_out, sql_out ,df_out])
    btn_flag.click(lambda *args: callback.flag(args), [inp, summ_out, sql_out, df_out], None, preprocess=False)

app.launch()