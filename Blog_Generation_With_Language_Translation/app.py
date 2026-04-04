import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from src.blog_generation_bot.graphs.blog_graph_builder import BlogGraphBuilder
from src.blog_generation_bot.llms.groq_model import GroqModel
from src.blog_generation_bot.llms.ollama_model import OllamaModel

os.environ['LANGSMITH_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
load_dotenv()

app = FastAPI()

#API's

@app.post("/blog")
async def create_blogs(request:Request):
    data = await request.json()
    topic = data.get("topic","")

    #get llm model

    llm = GroqModel().get_groq_model()

    #get the graph
    graph_obj = BlogGraphBuilder(llm=llm)
    graph = graph_obj.get_setup_graph(usecase="topic")
    state = graph.invoke({"topic": topic})

    return {"data":state}


if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
