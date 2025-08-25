from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.vectorstores import InMemoryVectorStore

loader = CSVLoader(
    file_path="RAG/tag.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["MLB Team", "Payroll in millions", "Wins"],
    },
)

data = loader.load()

# print(data)

##%pip install --quiet --upgrade langchain-text-splitters langchain-community langgraph


text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", chunk_size=100, chunk_overlap=0
)
texts = text_splitter.split_text(data)


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = getpass.getpass()

if not os.environ.get("DEEPSEEK_API_KEY"):
  os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter API key for DeepSeek: ")


llm = init_chat_model("deepseek-chat", model_provider="deepseek")

embeddings = DeterministicFakeEmbedding(size=4096)

vector_store = InMemoryVectorStore(embeddings)