import os
from dotenv import load_dotenv
load_dotenv()

# OpenAI API key (export OPENAI_API_KEY=xxxx in your shell)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Database (change credentials if needed)
DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:password@localhost:5432/coding_agent")
