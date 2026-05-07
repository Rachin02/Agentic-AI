
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from typing import Literal, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class academic_info(BaseModel):
    name: str
    subject: Literal['math', 'AI', 'database']
    marks: int
    grade: str
    teacher: str
    gender : Optional[str] = None


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


agent = create_agent(model,
                     response_format= academic_info,
                    system_prompt = 'you are a teacher and advisor of many student. you have to analysis each student information and their performance. if any information is not given mark them as unknown')


response = agent.invoke({
    'messages':[{'role':'user',
                 'content': 'Rachin is a man. rachin has got 83 in database course which is consider as A+. but his course teacher jahangir sir expected more from him,'}]
})


print(response['structured_response'])




# python3 C2-tools/structured_output.py