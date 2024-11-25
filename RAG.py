import os
import gradio as gr

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts.prompt import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

load_dotenv('.env')

OLLAMA_HOST = os.getenv('OLLAMA_HOST')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')

llm = OllamaLLM(
    base_url=OLLAMA_HOST,
    model=OLLAMA_MODEL
)

md_directory = "data/"
md_files = [f for f in os.listdir(md_directory) if f.endswith('.md')]

print(f"Markdown files: {md_files}")

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=250,
    length_function=len,
    is_separator_regex=False,
)

all_pages = []
for md_file in md_files:
    md_path = os.path.join(md_directory, md_file)
    loader = UnstructuredMarkdownLoader(md_path)
    pages = loader.load_and_split(text_splitter)
    all_pages.extend(pages)

    print(f"Content of {md_file}:")
    for page in pages:
        print(page)

    all_pages.extend(pages)
    print(f"Loaded {len(pages)} pages from {md_file}")

print(f"Total number of pages loaded: {len(all_pages)}")

embedding_model_nomic = OllamaEmbeddings(model="nomic-embed-text:latest")
db = Chroma.from_documents(all_pages, embedding_model_nomic)
retriever = db.as_retriever(search_kwargs={"k": 3})

template = """
Вы — учитель математики с искусственным интеллектом.
Ваша задача — создавать правильные математические задания на основе контекста.

### Контекст:
{context}

### Вопрос:
{input}

### Ответ:
"""

prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

def get_response(query: str) -> str:
    """
    Функция, возвращающая ответ на вопрос, основанный на текстовых данных.

    :param query: текст вопроса
    :return: текст ответа
    """
    response = retrieval_chain.invoke({"input": query})
    return response["answer"]

iface = gr.Interface(
  fn=get_response,
  inputs=gr.Textbox(lines=2, placeholder="Введите свой промпт..."),
  outputs=gr.Markdown(),
  title="llama",
  description="Напишите промпт на основе заданного контекста.",
)

iface.launch()
