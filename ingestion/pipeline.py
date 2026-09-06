from ingestion.github_loader import GitHubLoader
from ingestion.repository import RepositoryScanner
from ingestion.chunker import CodeChunker


class IngestionPipeline:
    def __init__(self):
        self.loader = GitHubLoader()
        self.scanner = RepositoryScanner()
        self.chunker = CodeChunker()

    def ingest(self, repo_url):
        # -----------------------------------------
        # 1. Clone repository
        # -----------------------------------------
        repository_path = self.loader.clone_repository(repo_url)

        # -----------------------------------------
        # 2. Scan repository
        # -----------------------------------------
        files = self.scanner.scan(repository_path)

        # -----------------------------------------
        # 3. Create code chunks
        # -----------------------------------------
        chunks = self.chunker.create_chunks(files)

        return {
            "repository_path": repository_path,
            "files": files,
            "chunks": chunks,
        }