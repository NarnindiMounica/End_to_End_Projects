import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from langchain_astradb import AstraDBVectorStore
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
#from datasets import load_dataset
#from PyPDF2 import PdfReader

load_dotenv()

st.title("PDF Query Using AstraDB Store")

uploaded_files = st.file_uploader("upload pdf to query", type="pdf", accept_multiple_files=True)
if uploaded_files:
    file_path = Path(__file__).parent
    for file in uploaded_files:
        with open(f"{file_path}/temppdf", "wb") as f:
            f.write(file.getvalue())

#document_loader and splitter to load pdf into document and split into smaller chunks

    loaded_docs = PyPDFLoader("temppdf").load()

    text_splitter=CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=100,
    length_function=len
    )

    chunks = text_splitter.split_documents(loaded_docs)

    #creating llm and embeddings

    model = ChatGroq(model="llama-3.1-8b-instant")
    embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

    #astra db vector store to store vectors

    astra_vector_store = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="my_collection",
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
        api_endpoint=f"https://{os.getenv("ASTRA_DB_ID")}-us-east1.apps.astra.datastax.com"
    )
    st.write("Astra DB is Ready ✅")

    #adding documents tp vector store

    astra_vector_store.add_documents(documents=chunks)

    #query the vector store
    user_query=st.text_input("Enter your question:")
    if user_query:
        results = astra_vector_store.similarity_search(user_query, k=2) 
        for result in results:
            st.success(f"Page : {result.metadata.page}\n Content: {result.page_content}")
    
#https://docs.langchain.com/oss/python/integrations/vectorstores/astradb
