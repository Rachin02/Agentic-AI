from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model = "gpt-5-nano",
    input = [
        {
            "role":"user",
            "content": "tell me all the avengers movies name."
        }
    ],
    stream = True
)

for event in stream:

    if event.type == "response.output_text.delta":
         print(event.delta, end = "", flush = True)

# python3 c3-dynamic-tool-calling/streaming.py