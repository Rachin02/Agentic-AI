from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import json
from langchain_core.tools import tool
load_dotenv()

# model = ChatOpenRouter(model="poolside/laguna-m.1:free")
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
model  = ChatOllama(model = "llama3.1")
# model = ChatOpenAI(model = "gpt-4o-mini-2024-07-18")


state = {
    "messages":[],
    "token":None
}

user = {
    "rachin": {
        "username":"rachin",
        "password":"12345"
    },
    "obito":{
        "username":"obito",
        "password":"76543"
    }
}

personal_data = {}


def write_json(filename, data):
    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 4)
    print(f"Data successfully save to {filename}")

def read_json(filename):
    with open(filename, 'r', encoding= 'utf-8') as file:
        return json.load(file)


@tool
def get_personal_data()-> str:
    ''' fetching personal data based on a given name. Only available to authenticated user '''
    print(f"[TOOL] accessing personal data")

    if state["token"] in personal_data:
        return personal_data[state["token"]]

    return f"you do not have any personal data. First add something" 

@tool
def add_personal_Data(data: str)-> str:
    ''' Only available to authenticated user '''
    print(f"[TOOL] adding personal data for {state["token"]}")

    if state["token"] in personal_data:
        personal_data[state["token"]] = personal_data[state["token"]] + data
        write_json("c3-dynamic-tool-calling/personal_data.json", personal_data)

        return f"Personal data add successfully for {state["token"]}"
    
    return f"You do not have permission to add personal data. please authenticate first"

@tool
def login_user(username:str, password:str)-> str:
    ''' passes username and password to authenticate user'''
    print(f"[TOOL] authenticating user -> username:{username} and password:{password}")

    if username.lower() in user and user[username.lower()]["password"] == password:
        state["token"] = username.lower()

        if state["token"] not in personal_data:
            personal_data[state["token"]] = ""
            write_json("c3-dynamic-tool-calling/personal_data.json", personal_data)


        return f"{username} authenticated successfully"
        
    return f"Invalid username and password. Please try again or register if you do not have an account"


@tool
def logout_user()-> str:
    '''Looging out current user'''
    print(f"[TOOL] logging out uesr {state["token"]}")

    state["token"] = None

    return f"User logout successfully"


@tool
def register_user(username: str, password:str) -> str:
    '''Register a new user using username and password'''
    print(f"[TOOL] is using to register a new user: {username}")

    if username.lower() in user:
        return f"Username already exist. Please choose a different username"
    
    user[username.lower()] = {
        "username": username.lower(),
        "password":password

    }

    personal_data[username.lower()]= ""
    return f"User: {username} register successfully. You can now login to access your data"

def load_conversation():
    print(f"[UTILITY] loading conversation....")

    try:
        with open('conversation.txt','r', encoding = 'utf-8') as file:
                content = file.read()
                state["messages"] = [{"role":"user", "content":f"Previous summary: {content}"}]
                return True
    except Exception as e:
        print(f"An error occur: {e}")
        return False

def save_conversation(summary: str):
    print(f"[UTILITY] saving conversation......")

    try: 
        with open('conversation.txt','w', encoding = 'utf-8') as file:
            file.write(summary)
            print(f"Successfully conversation saved to the file.")
    except Exception as e:
        print(f"An error occur while saving {e}")
        return False
    
    return True


def summarize_context():
    print(f"[UTILITY] summarizing conversation context....")

    agent = create_agent(model, system_prompt="Summarize the following conversation in a concise manner. Make sure to write all the historic details about the conversation, including user inputs and assistant responses. The summary should be comprehensive enough to provide context for future interactions without needing to refer back to the original messages. but not unnecessarily large.")

    result = agent.invoke({
        "messages":state["messages"]
    })

    summary = result["messages"][-1].content
    save_conversation(summary)
    return summary

    
def run_turn(user_input:str):

    if len(state["messages"]) > 4:
        summary = summarize_context()
        state["messages"] = [{"role":"user","content":f"summary of conversation: {summary}"}]

    state["messages"].append({"role":"user","content":user_input})

    print(f"User input: ",user_input)
    print(f"Current status: ", state)

    tools = []

    if state["token"]:
        tools.append(get_personal_data)
        tools.append(add_personal_Data)
        tools.append(logout_user)
    
    else:
        tools.append(login_user)
        tools.append(register_user)



    agent = create_agent(model, tools)

    result = agent.invoke({
        "messages": state["messages"]
    })

    state["messages"].append({"role":"ai","content":result["messages"][-1].content})
    
    print(f"Ai response: {result["messages"][-1].content}")


if __name__ == "__main__":

    if load_conversation():
        print(f"conversation load successfully.")

    personal_data_from_file = read_json("c3-dynamic-tool-calling/personal_data.json")
    print(f"Personal data from file: {personal_data_from_file}")

    if isinstance(personal_data_from_file, dict):
        personal_data.update(personal_data_from_file)
        print("Personal data loaded successfully.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit","quit"]:
            print("existing chat")
            break

        run_turn(user_input)

        print(f"-------------------------------------------------------------")


        # python3 c3-dynamic-tool-calling/dynamic_tools.py

