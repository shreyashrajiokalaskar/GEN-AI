import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama

MODEL = "llama3.2"

response = ollama.chat(
    model=MODEL, messages=[{"role": "user", "content": "Hello, who are you?"}]
)
# print(response['message']['content'])

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:

    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching {url}: {e}")

        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        body = soup.body
        if body:
            # Remove scripts, styles, images, inputs
            for irrelevant in body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = body.get_text(separator="\n", strip=True)
        else:
            self.text = ""


print("\n---------------------------------------\n")
ed = Website("https://shreyash-kalaskar.netlify.app")
# print(ed)

print("\n---------------------------------------\n")

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# print(user_prompt_for(ed))


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]


def summarize(url):
    website = Website(url)
    response = ollama.chat(model=MODEL, messages=messages_for(website))
    return response["message"]["content"]


def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))


display_summary("https://cnn.com")

# system_prompt2 = "You are an assistant that gives information about the components of an airplane and provides a short summary."
# THIS USES THE MODIFIED SYSTEM_PROMPT
# component = input("Ask the bot!")
# response = ollama.chat(
#     model=MODEL,
#     messages=[
#     {"role": "system", "content": system_prompt2},
#     {"role": "user", "content": f"What is {component}" }
#     ]
# )
# print(response['message']['content'])
