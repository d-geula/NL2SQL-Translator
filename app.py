from pathlib import Path

import gradio as gr
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# Define some example queries
examples = [
    ["How many players are there with a first name that begins with 'John'?"],
    ["Is steph curry active?"],
    ["List all players with a last name of Jordan"],
]


# Main function
def nl_to_sql(prompt: str):
    db_path = "files/nba.sqlite"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=2)
    llm = OpenAI(temperature=0, verbose=False)  # type: ignore

    db_chain = SQLDatabaseChain.from_llm(
        llm, db, verbose=False, return_intermediate_steps=True
    )

    result = db_chain(prompt)

    sql_query = result["intermediate_steps"][1]
    data = eval(result["intermediate_steps"][3])
    summary = result["intermediate_steps"][5]

    return summary, sql_query, data


callback = (
    gr.CSVLogger()
)  # See docs: https://gradio.app/using-flagging/#flagging-with-blocks

with gr.Blocks() as app:
    gr.Markdown(Path("description.md").read_text())

    with gr.Row():
        with gr.Column():
            summ_out = gr.Textbox(lines=3, interactive=False, label="Data summary:")
            inp = gr.Textbox(
                placeholder="What would you like to know?", lines=1, label="Question:"
            )
            with gr.Row():
                btn_run = gr.Button("Submit", variant="primary")
                btn_flag = gr.Button("Flag")
            gr.Examples(examples, inp)

    with gr.Row():
        with gr.Accordion("Raw Data", open=False):
            sql_out = gr.TextArea(
                lines=1, interactive=False, label="SQL query:"
            )  # Probably unnecessary other than for debugging
            df_out = gr.DataFrame(interactive=False)

    callback.setup([inp, summ_out, sql_out, df_out], "flagged_data_points")

    btn_run.click(fn=nl_to_sql, inputs=inp, outputs=[summ_out, sql_out, df_out])
    btn_flag.click(
        lambda *args: callback.flag(args),
        [inp, summ_out, sql_out, df_out],
        None,
        preprocess=False,
    )

app.launch()
