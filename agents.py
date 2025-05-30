import requests

from openai import OpenAI

PLAN_PROMPT = """
You are a planning agent. Given a user input, classify it using only one of the following tasks:
summarize, define, compare, quiz, lookup

Respond with just the task name.
Input: {query}
Task:
"""


client = None  # Global client to reuse

def ensure_client(api_key):
    global client
    if client is None:
        client = OpenAI(api_key=api_key)
    return client


def plan_task(query, api_key):
    ensure_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PLAN_PROMPT.format(query=query)}
        ]
    )
    task_raw = response.choices[0].message.content.strip().lower()

   
    for prefix in ["task:", "-", "–", "*"]:
        if task_raw.startswith(prefix):
            task_raw = task_raw[len(prefix):].strip()

    return task_raw


    for prefix in ["task:", "-", "–", "*"]:
        if task_raw.startswith(prefix):
            task_raw = task_raw[len(prefix):].strip()

    return task_raw

def run_summarizer(query, api_key):
    ensure_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following text:"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()


def run_definer(query, api_key):
    ensure_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Define the concept in simple terms:"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()


def run_comparator(query, api_key):
    ensure_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Compare the following concepts:"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()


def run_lookup(query, api_key=None):
    try:
        response = requests.get("http://localhost:8000/wikipedia", params={"query": query})
        if response.status_code == 200:
            data = response.json()
            summary = data.get("summary", "No summary available.")
            title = data.get("title", "Wikipedia Page")
            url = data.get("url", "#")
            return f"### [{title}]({url})\n\n{summary}"
        else:
            return f"Wikipedia error: {response.json().get('error', 'Unknown error')}"
    except Exception as e:
        return f"Failed to fetch from Wikipedia tool: {e}"

def run_quizzer(query, api_key):
    ensure_client(api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate quiz questions based on this text:"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()


agent_map = {
    "summarize": run_summarizer,
    "define": run_definer,
    "compare": run_comparator,
    "quiz": run_quizzer,
    "lookup": run_lookup
}
