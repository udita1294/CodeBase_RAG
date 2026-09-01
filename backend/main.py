import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

from ingestion.github_loader import GitHubLoader
from ingestion.repository import RepositoryScanner


load_dotenv()

app = FastAPI(title="Codebase RAG", description= "AI Software Engineer for understanding GitHub repositories", version= "0.1.0")

class RepositoryRequest(BaseModel):
    repo_url: str


@app.get("/")
def root():
    return {"message": "Welcome to Codebase RAG!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/repository/analyze")
def analyze_repository(request: RepositoryRequest):
    loader = GitHubLoader()
    repository_path = loader.clone_repository(request.repo_url)
    scanner = RepositoryScanner()
    files = scanner.scan(repository_path)

    return {
        "repository_url": request.repo_url,
        "total_files": len(files),
        "files": files
    }


