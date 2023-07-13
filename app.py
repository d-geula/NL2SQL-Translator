from pathlib import Path

import gradio as gr

from nl2sql.sql_chain import sql_chain


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
            sql_query = gr.TextArea(
                lines=1, interactive=False, label="SQL query:"
            )  # Probably unnecessary other than for debugging
            sql_results = gr.DataFrame(interactive=False)

    callback.setup([inp, answer_out, sql_query, sql_results], "flagged_data_points")

    btn_run.click(
        fn=sql_chain, inputs=inp, outputs=[answer_out, sql_query, sql_results]
    )
    btn_flag.click(
        lambda *args: callback.flag(args),  # type: ignore
        [inp, answer_out, sql_query, sql_results],
        None,
        preprocess=False,
    )

app.launch()
