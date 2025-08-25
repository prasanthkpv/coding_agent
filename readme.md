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

<!-- API_KEY="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"
z-AI :"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"
deepseek:"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" -->