import openai
from os import getenv


openai.api_key = getenv("OPENAI_API_KEY")


def get_answer(model_name, text):
    if model_name == 'Chat':
        return chat(text)
    if model_name == 'Friend chat':
        return friend_chat(text)
    if model_name == 'Explain code':
        return explain_code(text)


def chat(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response['choices'][0]['text']


def friend_chat(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
    return response['choices'][0]['text']


def explain_code(text):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=text,
      temperature=0,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\"\"\""]
    )
    return response['choices'][0]['text']
