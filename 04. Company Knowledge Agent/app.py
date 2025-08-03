import warnings
warnings.filterwarnings("ignore")

import os
import glob
import gradio as gr
from IPython.display import Markdown, display
import shutil
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import plotly.graph_objects as go
from langchain.memory import ConversationBufferMemory,ChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
import logging
from langchain_core.runnables import RunnableParallel
from operator import itemgetter
from pydantic import BaseModel, Field
from datetime import datetime
import json
from pathlib import Path
from threading import Thread


def add_metadata(doc, doc_type):
    doc.metadata["doc_type"] = doc_type
    return doc

# Adjusting utf-8 
text_loader_kwargs = {'encoding': 'utf-8'}

# Path to folder with the files
folders = glob.glob("knowledge-base/*")

# Embeddings open source
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

# Loading vector store
db_name = "vector_db"
vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)

# Path to folder with the files
folders = glob.glob("knowledge-base/*")

# The vectors
collection = vectorstore._collection
count = collection.count()

sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)
print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")

# Prework 
result = collection.get(include=['embeddings', 'documents', 'metadatas'])
vectors = np.array(result['embeddings'])
documents = result['documents']
metadatas = result['metadatas']
doc_types = [metadata['doc_type'] for metadata in metadatas]
colors = [['blue', 'green', 'red', 'orange'][['model', 'motoboys', 'services', 'company'].index(t)] for t in doc_types]

# MODEL = "llama3.2"
MODEL = "phi3"

# create a new Chat with llama3.2
llm = ChatOpenAI(temperature=0.7, model_name=MODEL, base_url='http://localhost:11434/v1', api_key='ollama')

# set up the conversation memory for the chat, in case we want LLM to respond considering previous questions
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key="answer")

# the retriever is an abstraction over the VectorStore that will be used during RAG
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# putting it together: set up the conversation chain with the MODEL, the vector store and memory
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever,return_source_documents=True, output_key="answer")

# Feedback Saving
class FeedbackEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_query: str
    model_response: str
    feedback: str
    source_documents: list[str]

FEEDBACK_LOG = Path("feedback_log.jsonl")

def save_feedback_async(entry: FeedbackEntry):
    logging.info("Feedback Saved")
    def _save():
        with FEEDBACK_LOG.open("a") as f:
            f.write(entry.model_dump_json() + "\n")
    Thread(target=_save).start()

last_interaction = {"query": "", "answer": "", "sources": []}

def generate_response(message, history):
    result = conversation_chain({"question": message,"chat_history":[]})
    answer = result["answer"]
    sources = [doc.page_content for doc in result["source_documents"]]

    documents = result.get("source_documents", [])
    top_docs = documents[:2]
    doc_names = []
    for i, doc in enumerate(top_docs, 1):
        source = doc.metadata.get("source", f"Documento {i}")
        filename = source.split("/")[-1]
        doc_names.append(f"{i}. {filename}")

    rag_list = "\n".join(doc_names)

    last_interaction["query"] = message
    last_interaction["answer"] = answer
    last_interaction["sources"] = sources

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return "", history,rag_list

def register_feedback(feedback_type):
    entry = FeedbackEntry(
        user_query=last_interaction["query"],
        model_response=last_interaction["answer"],
        feedback=feedback_type,
        source_documents=last_interaction["sources"]
    )
    save_feedback_async(entry)
    return f"Feedback '{feedback_type}' registered sucessfully."

# Chat Interface - Gradio

# User interface
with gr.Blocks() as ui:
    gr.Markdown("## 💬 LLM Deliveries Internal Chat")

    with gr.Row():
        with gr.Column(scale=4):  # Chat 
            chatbot = gr.Chatbot(type="messages")

            with gr.Row():  # Input + buttons
                msg = gr.Textbox(placeholder="Type your question...",  show_label=False, scale=9)
                with gr.Column(scale=1, min_width=60):
                    send_btn = gr.Button("➤", size="sm")

        with gr.Column(scale=1): 
            gr.Markdown("### Feedback")
            thumbs_up = gr.Button("👍 (Good Answer)")
            thumbs_down = gr.Button("👎 (Bad Answer)")
            feedback_status = gr.Textbox(label="Feedback Status")

            gr.Markdown("### Relevant Documents")
            rag_docs = gr.Textbox(lines=6, interactive=False, label=None)

    send_btn.click(generate_response, inputs=[msg, chatbot], outputs=[msg, chatbot, rag_docs])
    msg.submit(generate_response, inputs=[msg, chatbot], outputs=[msg, chatbot, rag_docs])
    thumbs_up.click(fn=lambda: register_feedback("thumbs_up"), outputs=feedback_status)
    thumbs_down.click(fn=lambda: register_feedback("thumbs_down"), outputs=feedback_status)

ui.launch(inbrowser = True)
