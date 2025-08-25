coding_agent/
├── agent.py          # Main coding agent logic
├── api.py            # REST API
├── db.py             # Postgres DB models
├── config.py         # Config & API keys
├── tools/            # Utilities (code exec, lint, git, etc.)
│   ├── code_exec.py
│   ├── lint.py
│   └── git_ops.py
└── requirements.txt


# Make project folder
mkdir coding_agent && cd coding_agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install libraries
pip install openai flask sqlalchemy psycopg2 requests rich

## App Image:
![app image](images/app-screenshot.png)


<!-- API_KEY="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"
z-AI :"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"
deepseek:"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" -->
langSmith APU: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
pip install -U langchain langchain-openai
project name:pr-fixed-someplace-31
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="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"
LANGSMITH_PROJECT="pr-fixed-someplace-31"
OPENAI_API_KEY="<your-openai-api-key>"
GEMNI_API_KEY="AIzaSyBVP8LRAuC_VRhHGfj30xhEN5mjmqxj9kw"