import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OpenKey = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=OpenKey
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an Indonesian teacher."},
    {"role": "user", "content": "apa itu gaya dalam fisika?"}
  ]
)

print(completion.choices[0].message.content)
