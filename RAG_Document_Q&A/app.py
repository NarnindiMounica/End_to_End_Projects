import os
import langchain
import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")

def retriever_ready(file_path):
    st.session_state.loader = PyPDFDirectoryLoader(file_path)
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    st.session_state.chunks = st.session_state.splitter.split_documents(st.session_state.docs)
    st.session_state.embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    st.session_state.store = FAISS.from_documents(documents=st.session_state.chunks , embedding=st.session_state.embeddings)


st.title("RAG DOCUMENT Q&A BOT")  

if st.button("Getting Retriever Ready"):
    retriever_ready(file_path='research_papers/')
    st.write("Retriever is loaded")

user_query = st.text_input("Enter your query..")

if user_query:

    retriever = st.session_state.store.as_retriever()
    
    llm = ChatGroq(model="llama-3.1-8b-instant")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
             """you are a qa bot, answer the question based only on given context information.
               If their is not context for a question mention the same do not answer on your own.
                {context}"""),

            ("user", "{input}")    
        ]
    )
    documents_chain = create_stuff_documents_chain(llm, prompt)

    retriever_chain = create_retrieval_chain(retriever, documents_chain)

    response = retriever_chain.invoke({"input": user_query})
    st.success(response['answer'])

    st.expander("Relevant support documents")
    for i , docs in enumerate(response['context']):
        st.write(docs.page_content)
        st.write(20*"--")

    









