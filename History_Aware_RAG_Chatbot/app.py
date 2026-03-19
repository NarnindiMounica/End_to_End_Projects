import os
import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains import create_history_aware_retriever

from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

groq_api_key= os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')

if groq_api_key:
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)
    st.sidebar.write("Model loaded successfully ✅ ")

st.title("⏳ History Aware RAG BOT 🧠")

loaded_files=st.file_uploader("Upload a file to query it", type="pdf", accept_multiple_files=True)
if loaded_files is not None:
    temp_file = "tmp_pdf"
    for file in loaded_files:
        with open(temp_file, "wb") as f:
            f.write(file.getvalue())
            st.sidebar.success(f"{file.name} is successfully uploaded to query")

    documents = PyPDFLoader(temp_file).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
    retriever = vector_store.as_retriever()
    st.sidebar.success("Retriever is ready")

    rephrase_prompt = ChatPromptTemplate.from_messages([
        ("system","""
        Given chat history and latest user question which might reference context
        in the chat history formulate a standalone question which can be understood without chat history.
        Don't answer the question, just reformulate it if needed otherwise return it as it is.
        """),
        MessagesPlaceholder(variable_name="message_history"),
        ("human", '{input}')
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, 
        retriever, 
        rephrase_prompt
    )

    qa_sys_prompt = """ You are an assistant for question-answering task.
         use the following piece of retrieved context to answer the question.
         If you don't know the answer,  say that you don't know. Use three
         sentences maximum and keep the answer concise.
         <context>
         {context}
         </context>"""
    context_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_sys_prompt),
        MessagesPlaceholder(variable_name="message_history"),
        ("human", '{input}')]
    )

    document_chain = create_stuff_documents_chain(llm, context_prompt)
    retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    store = {}
    
    def get_session_state(id:str)->BaseChatMessageHistory:
        if id not in store.keys():
            store[id] = ChatMessageHistory()
        return store[id]
    
    with_message_history = RunnableWithMessageHistory(retrieval_chain, get_session_state)







