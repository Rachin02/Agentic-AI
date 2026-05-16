from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()


def get_weather(data:str):
    """ Get weather for a given city"""

    return f"It's  always sunny in {data}"


agent = create_agent(
    model="gpt-5-nano",
    tools = [get_weather]
)

# for chunk in agent.stream(
#     {"messages":  [{"role":"user", "content":"What is the weather in dhaka?"}]},
#     stream_mode="updates",
#     version="v2" ):

#     if chunk["type"] == "updates":
#         for step, data in chunk["data"].items():
#             print(f"step: {step}")
#             print(f"content: {data['messages'][-1].content_blocks}")


for chunk in agent.stream(
    {"messages":  [{"role":"user", "content":"What is the weather in dhaka?"}]},
    stream_mode="messages",
    ):

    message_chunk, metadata = chunk

    if message_chunk.content:
        print(message_chunk.content, end = "", flush = True)
# python3 c3-dynamic-tool-calling/langchain_streaming.py