import os
from dotenv import load_dotenv
load_dotenv()

import nest_asyncio 
nest_asyncio.apply()

# bring in deps
from llama_parse import LlamaParse 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

llamapars_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
parser = LlamaParse(
  api_key=llamapars_api_key,
  result_type="markdown"
)

file_extractor = {"pdf": parser}
documents = SimpleDirectoryReader(input_files=['data/gpt4_report.pdf'], file_extractor=file_extractor).load_data()

documents 

documents[0].text[:200]

##----------- Ollama Model -----------

# by default llamaindex uses OpenAI models
from llama_index.embeddings.ollama import OllamaEmbedding

embed_model = OllamaEmbedding(
    #model_name="nomic-embed-text",
    model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

from llama_index.llms.ollama import Ollama  # noqa: E402
llm = Ollama(model="llama2", request_timeout=30.0)

from llama_index.core import Settings  # noqa: E402

Settings.llm = llm
Settings.embed_model = embed_model

# get the answer out of it
# create an index from the parsed markdown
index = VectorStoreIndex.from_documents(documents)

# create a query engine for the index
query_engine = index.as_query_engine()

# query the engine
from IPython.display import Markdown, display  # noqa: E402

# query the engine
query = "what is the BoolQ value of GPT4All-J 6B v1.0* model ?"
response = query_engine.query(query)
display(Markdown(f"<b>{response}</b>"))