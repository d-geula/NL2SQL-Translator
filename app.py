from pathlib import Path

import pandas as pd
import gradio as gr

from nl2sql.utils import extract_columns, format_query
from nl2sql.sql_chain import sql_chain
from nl2sql.enhanced_summary import enhanced_summary


def handle_input(input: str):
    _, sql_query, sql_results = sql_chain(input)

    docs = Path("docs/martin_brundle.txt").read_text()

    formatted_query = format_query(sql_query)
    df = pd.DataFrame(sql_results, columns=extract_columns(sql_query))
    summary = enhanced_summary(docs, input, sql_results)

    return summary, formatted_query, df


examples = [
    ["List all swedish drivers?"],
    ["How many drivers are there born after 1995?"],
    ["Who is the youngest driver?"],
]

callback = (
    gr.CSVLogger()
)  # See docs: https://gradio.app/using-flagging/#flagging-with-blocks

with gr.Blocks() as app:
    # gr.Markdown(Path("description.md").read_text())

    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(
                placeholder="What would you like to know?", lines=1, label="Question:"
            )
            answer_out = gr.Textbox(lines=3, interactive=False, label="Answer:")
            with gr.Row():
                btn_run = gr.Button("Submit", variant="primary")
                btn_flag = gr.Button("Flag")
            gr.Examples(examples, inp)

    with gr.Row():
        with gr.Accordion("Raw Data", open=False):
            sql_query = gr.Markdown()
            sql_results = gr.DataFrame(interactive=False)

    callback.setup([inp, answer_out, sql_query, sql_results], "flagged_data_points")

    btn_run.click(
        fn=handle_input, inputs=inp, outputs=[answer_out, sql_query, sql_results]
    )
    btn_flag.click(
        lambda *args: callback.flag(args),  # type: ignore
        [inp, answer_out, sql_query, sql_results],
        None,
        preprocess=False,
    )

app.launch()
