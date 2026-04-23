import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent


os.environ["GOOGLE_API_KEY"] = "AIzaSyC8M2TgVr3bpoWO1VkVTUDLA2HqevZhF0I"

model = ChatGoogleGenerativeAI(model ="gemini-2.5-flash-lite")

agent = create_agent(model)

response = agent.invoke({
    "messages":[("user","I am Rachin"),
               ("ai","Hello rachin"),
               ("user","what is my name")]
})


# print(response)

print(response["messages"][-1].content)


#. python3 C1-connectingAPI/tmp2.py