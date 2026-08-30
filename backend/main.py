from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Codebase RAG", description= "AI Software Engineer for understanding GitHub repositories", version= "0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to Codebase RAG!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


