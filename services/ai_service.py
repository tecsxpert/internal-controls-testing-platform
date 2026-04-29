import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_prompt(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content