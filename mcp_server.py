from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents import run_summarizer, run_lookup, run_definer, run_comparator, run_quizzer
from langsmith import traceable
import os

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    api_key: str = os.getenv("OPENAI_API_KEY")  

@app.post("/summarize")
@traceable(name="summarize")
def summarize(req: QueryRequest):
    return {"result": run_summarizer(req.query, req.api_key)}

@app.post("/define")
@traceable(name="define")
def define(req: QueryRequest):
    return {"result": run_definer(req.query, req.api_key)}

@app.post("/compare")
@traceable(name="compare")
def compare(req: QueryRequest):
    return {"result": run_comparator(req.query, req.api_key)}

@app.post("/quiz")
@traceable(name="quiz")
def quiz(req: QueryRequest):
    return {"result": run_quizzer(req.query, req.api_key)}

@app.post("/lookup")
@traceable(name="lookup")
def lookup(req: QueryRequest):
    return {"result": run_lookup(req.query)}
