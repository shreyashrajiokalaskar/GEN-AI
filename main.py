import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")
client = OpenAI(api_key=api_key)

# if MODEL == "":
#     print("COULD NOT LOAD MODEL")
# print("MODEL", MODEL)
system_prompt = "You are a helpful assistant that responds in markdown"


def mssg_gtp(prompt):
    response = client.chat.completions.create(
        model=(MODEL or "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


def stream_mssg_gtp(prompt):
    stream = client.chat.completions.create(
        model=(MODEL or "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


print(mssg_gtp("What is today's date?"))


def shout(txt):
    return str(txt).upper()


# gr.Interface(
#     fn=shout, inputs="textbox", outputs="textbox", allow_flagging="never"
# ).launch()

# view = gr.Interface(
#     fn=mssg_gtp,
#     inputs=[gr.Textbox(label="Enter your mssg here", lines=6)],
#     outputs=[gr.Textbox(label="Response:", lines=6)],
#     flagging_mode="never",
#     show_progress="full",
# )

# view.launch()

view = gr.Interface(
    fn=stream_mssg_gtp,
    inputs=[gr.Textbox(label="Enter your mssg here", lines=6)],
    outputs=gr.Markdown(label="Response:"),
    flagging_mode="never",
    show_progress="full",
)

view.launch()
