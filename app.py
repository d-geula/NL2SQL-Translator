
import gradio as gr
import utils

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

    return f"Query used: {sql_query}\n\n{query_description}", query_result


with gr.Blocks() as app:

    # gr.Markdown("Start typing below and then click **Run** to see the output.")

    with gr.Row():
        inp = gr.Textbox(placeholder="What would you like to know?", lines=1, label="Question:")
        out = gr.Textbox(lines=1, label="Data summary:")
    df_out = gr.DataFrame(label="Query Results:")

    btn = gr.Button("Execute query")
    btn.click(fn=nl_to_sql, inputs=inp, outputs=[out, df_out])

    gr.Examples(
        ["How many players are there with a first name that begins with 'John'?",
         "Is steph curry active?",
         "List all players with a last name of Jordan?"],
        inp
    )

app.launch()