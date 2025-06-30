import json
import os
import requests
from bs4 import BeautifulSoup, Tag
from IPython.display import Markdown, display
from openai import OpenAI
from dotenv import load_dotenv

MODEL = "gpt-4o-mini"
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)


class Website:

    def __init__(self, url):
        self.url = url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

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
        self.links = [
            link.get("href")
            for link in soup.find_all("a")
            if isinstance(link, Tag) and link.get("href")
        ]

    def get_contents(self):
        return f"Webpage title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


# ed = Website("https://shreyash-kalaskar.netlify.app")
# print(ed.links)

system_prompt = "You are provided with a list of links found on a webpage. You are able to decide which of the links would be most relevant to include in a brochure about a company, such as links to About page, or a Company page, or a Careers/Jobs pages.\n"
system_prompt += "You should response in JSON as in this example:"
system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about},
        {"type": "careers page", "url": "https://another.full.url/goes/here/careers}
        
    ]
}
"""


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


# print(get_links_user_prompt(ed))


def get_links(url):
    website = Website(url)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result or "")


def get_all_details(url):
    result = "Landing Page:\n"
    result = Website(url).get_contents()
    links = get_links(url)
    print("HERE are links\n", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        try:
            result += Website(link["url"]).get_contents()
        except:
            print("GOT AN ERROR!")

    return result


# print(get_links("https://shreyash-kalaskar.netlify.app"))
# print(get_links("https://huggingface.co"))

# print(get_all_details("https://anthropic.com"))


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
    return user_prompt


def translate_to_lang(lang, prompt):
    symtem_promp = f"You are a translator with expertise in translating company brochure to other languages. Translate the brochure in other languages and respond in markdown"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": symtem_promp},
            {
                "role": "user",
                "content": f"Translate this company brochure to {lang}\n{prompt}",
            },
        ],
        stream=True,
    )
    full_content = ""
    for chunk in response:
        # Access the streamed delta content
        delta = chunk.choices[0].delta
        if hasattr(delta, "content"):
            part = delta.content
            full_content += part or ""
            print(part, end="")  # streaming output
    # Finally, do something with the full content
    print("\n\n=== FULL CONTENT ===\n")
    print(full_content)
    display(Markdown(full_content))


def create_brochure(company_name, url):
    system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits in a funny way. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    translate_to_lang("Marathi", response.choices[0].message.content)

    # result = response["message"]["content"]
    # print(result)
    # display(Markdown(result))


create_brochure("ShreyashKalaskar", "https://shreyash-kalaskar.netlify.app")
