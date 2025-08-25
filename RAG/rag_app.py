import bs4
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import DeterministicFakeEmbedding
from langsmith import Client
from dotenv import load_dotenv
from IPython.display import Image, display
from PIL import Image as PILImage
import io
from langchain.chat_models import init_chat_model
load_dotenv()

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# print(f"Split blog post into {len(all_splits)} sub-documents.")

embeddings = DeterministicFakeEmbedding(size=4096)

vector_store = InMemoryVectorStore(embeddings)
document_ids = vector_store.add_documents(documents=all_splits)

# Create a LANGSMITH_API_KEY in Settings > API Keys
os.environ["LANGSMITH_TRACING"] = "true"

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
prompt = client.pull_prompt("rlm/rag-prompt", include_model=True)

example_messages = prompt.invoke(
    {"context": "(context goes here)", "question": "(question goes here)"}
).to_messages()

# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  #"AIzaSyBVP8LRAuC_VRhHGfj30xhEN5mjmqxj9kw"
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


display(Image(graph.get_graph().draw_mermaid_png()))

png_bytes = graph.get_graph().draw_mermaid_png()

# Save to file
with open("images/graph.png", "wb") as f:
    f.write(png_bytes)
# Or open directly
PILImage.open(io.BytesIO(png_bytes)).show()

response = graph.invoke({"question": "What is Task Decomposition?"})
print("Answer:", response["answer"])


for step in graph.stream(
    {"question": "What is Task Decomposition?"}, stream_mode="updates"
):
    print(f"{step}\n\n----------------\n")

for message, metadata in graph.stream(
    {"question": "What is Task Decomposition?"}, stream_mode="messages"
):
    print(message.content, end="|")