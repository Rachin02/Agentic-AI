from google import genai
from pydantic import BaseModel
from typing import Literal, Optional
from dotenv import load_dotenv
load_dotenv()

class Academic_info(BaseModel):
    name: str
    subject: Literal['math', 'AI', 'database']
    marks: int
    grade: str
    teacher: str
    gender : Optional[str] = None

    
client = genai.Client()

prompt = 'rachin has got 83 in database course which is consider as A+. but his course teacher jahangir sir expected more from him. So he is starting working hard agains'

response = client.models.generate_content(
    model = 'gemini-2.5-flash-lite',
    contents = prompt,
    config = {
        'response_mime_type':'application/json',
        'response_json_schema':Academic_info.model_json_schema()
    }
)

ans = Academic_info.model_validate_json(response.text)

print(ans)

# python3 C2-tools/structured_output0.py