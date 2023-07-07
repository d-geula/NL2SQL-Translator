from pathlib import Path

import gradio as gr
from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.llms.fake import FakeListLLM


def nl_to_sql(input: str, _test: bool = False):
    db_path = "db/formula1.sqlite"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)

    if not _test:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, verbose=True)  # type: ignore
    else:
        response = [
            'SELECT "forename", "surname" FROM drivers WHERE "nationality" = \'Swedish\' LIMIT 5;',
            "Stefan Johansson, Slim Borgudd, Ronnie Peterson, Gunnar Nilsson, Conny Andersson",
        ]
        llm = FakeListLLM(responses=response)

    db_chain = SQLDatabaseChain.from_llm(
        llm, db, verbose=True, return_intermediate_steps=True
    )

    result = db_chain(input)

    sql_query = result["intermediate_steps"][1]
    data = eval(result["intermediate_steps"][3])
    summary = result["intermediate_steps"][5]

    return summary, sql_query, data


examples = [
    ["List all swedish drivers?"],
    ["How many drivers are there born after 1995?"],
    ["Who is the youngest driver?"],
]

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
        lambda *args: callback.flag(args),  # type: ignore
        [inp, summ_out, sql_out, df_out],
        None,
        preprocess=False,
    )

app.launch()
