from openai import OpenAI
from db import SessionLocal, Task
from tools import code_exec, lint
import os

# openai.api_key = config.OPENAI_API_KEY
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENAI_API_KEY"),
)

class CodingAgent:
    def __init__(self):
        self.db = SessionLocal()

    def handle_request(self, prompt: str) -> str:
        # 1. Ask LLM
        # response = openai.ChatCompletion.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system", "content": "You are a coding assistant."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        # answer = response.choices[0].message["content"]

        response = client.chat.completions.create(
            # extra_headers={
            #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            # },
            extra_body={},
            model="z-ai/glm-4.5-air:free",    #"tngtech/deepseek-r1t2-chimera:free",
            messages=[
                {"role": "system", "content": "You are a coding assistant. Provide only the code, no instruction to run or execute."},
                {"role": "user", "content": prompt}
            ]
            )

        answer = response.choices[0].message.content

        # 2. Store in DB
        task = Task(query=prompt, response=answer)
        self.db.add(task)
        self.db.commit()

        return answer

    def run_code(self, code: str) -> str:
        return code_exec.run_code(code)

    def lint_code(self, code: str) -> str:
        return lint.lint_code(code)
