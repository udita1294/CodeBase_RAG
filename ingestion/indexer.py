from embeddings.embedder import CodeEmbedder
from vector_store.qdrant_store import QdrantStore
from ingestion.pipeline import IngestionPipeline

class RepositoryIndexer:
    def __init__(self, collection_name):
        self.pipeline = IngestionPipeline()
        self.embedder = CodeEmbedder()
        self.store = QdrantStore(collection_name=collection_name)

    def index_repository(self, repo_url):
        result = self.pipeline.ingest(repo_url)
        chunks = result["chunks"]
        if not chunks:
            return {
                "files": len(result["files"]),
                "chunks": 0
            }

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.embedder.embed(texts)

        self.store.create_collection(vector_size=len(embeddings[0]))
        self.store.add_chunks(chunks,embeddings)

        return {
            "files": len(result["files"]),
            "chunks": len(chunks)
        }