import os
from typing import cast
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print(
        "No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!"
    )
elif not api_key.startswith("sk-proj-"):
    print(
        "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook"
    )
elif api_key.strip() != api_key:
    print(
        "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook"
    )
else:
    print("API key found and looks good so far!")

client = OpenAI(
    api_key=api_key,
)

MODEL = "gpt-4o-mini"


system_prompt = "You are a Tutor who answers questions related to AI and ML only. When questions outside this domain are asked, politely apologize and inform the user that the topic is outside your expertise. Your response must always be in Markdown format."
conversation = [
    {"role": "system", "content": system_prompt},
]
messages = cast(list[ChatCompletionMessageParam], conversation)


def send_prompt(system_prompt, user_prompt, stream=False):
    conversation.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response


def get_answer(question):
    answer = send_prompt(system_prompt, question, False)
    result = answer.choices[0].message.content
    conversation.append({"role": "assistant", "content": cast(str, result)})
    print(result)
    display(Markdown(result))


print("Hello this is your Tutor for AI and ML!")

while True:
    question = input("Please ask doubts incase you have any, else type exit to exit!\n")
    if question != "exit":
        answer = get_answer(question)

    else:
        break
