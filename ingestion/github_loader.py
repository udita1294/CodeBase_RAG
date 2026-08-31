import os
import shutil
from pathlib import Path
from git import Repo

class GitHubLoader:
    def __init__(self, base_path = "data/repositories"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def clone_repository(self, repo_url:str) -> str:
        repo_name = repo_url.rsplit('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        repo_path = self.base_path / repo_name

        # remove the existing repository if it exists
        if repo_path.exists():
            shutil.rmtree(repo_path)

        Repo.clone_from(repo_url, repo_path)
        print(f"Cloning repository {repo_url} to {repo_path}")

        return str(repo_path)
        