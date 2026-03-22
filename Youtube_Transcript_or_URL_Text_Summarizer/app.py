import streamlit as st
import validators
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import load_summarize_chain
from langchain_core.documents import Document



st.title("➡️Summarize Youtube Video Transcript or URL🌍")

with st.sidebar:
    st.title("Settings")
    groq_api_key = st.sidebar.text_input("Enter your groq api key", type="password") 

#defining function to return loaded documents based on url type

def get_documents(user_url:str)->Document:
    #to validate given url
    try:
        if validators.url(user_url):
            st.success("Valide URL, Loading Summary..")     
            if "youtube.com" in user_url:
                try:
                    docs = YoutubeLoader.from_youtube_url(user_url, add_video_info=True).load()
                    chunks = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100).split_documents(docs)
                except :
                    st.error("Transcript not available for this url.") 
                    return None   
            else:
                docs = UnstructuredURLLoader(urls=[user_url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0"}).load()
                chunks = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100).split_documents(docs)
        return chunks 
    except Exception as e:
        st.error(f"Error loading URL {e}") 
        return None

user_url=st.text_input("Enter your url link to get summary of it")
final_documents=get_documents(user_url=user_url)
if user_url and final_documents is not None:
    
    model = ChatGroq(groq_api_key=groq_api_key, model="llama-3.1-8b-instant")
    chain_prompt = PromptTemplate(
        template="Summarize given text in less than 300 words {text}"
    )
    summarize_chain = load_summarize_chain(
        llm=model,
        chain_type="stuff",
        verbose=True,
        prompt=chain_prompt)


    result = summarize_chain.run(final_documents)
    st.write(result)









