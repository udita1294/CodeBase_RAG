from embeddings.embedder import CodeEmbedder
from vector_store.qdrant_store import QdrantStore


class CodeRetriever:
    def __init__(self,collection_name="codebase"):
        self.embedder = CodeEmbedder()
        self.vector_store = QdrantStore(collection_name=collection_name)

    def retrieve(self,query,top_k=5):
        # Convert question into embedding
        query_vector = self.embedder.embed([query])[0]
        # Search Qdrant
        results = self.vector_store.search(query_vector=query_vector,limit=top_k)

        return results