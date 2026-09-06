import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (Distance,VectorParams,PointStruct)

load_dotenv()

class QdrantStore:
    def __init__(self,collection_name="codebase"):
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url:
            raise ValueError("QDRANT_URL is not set in .env")

        if not qdrant_api_key:
            raise ValueError("QDRANT_API_KEY is not set in .env")

        self.client = QdrantClient(url=qdrant_url,api_key=qdrant_api_key,)
        self.collection_name = collection_name

    # --------------------------------------------------
    # Create collection
    # --------------------------------------------------
    def create_collection(self,vector_size):
        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_collections:
            self.client.create_collection(
                collection_name = self.collection_name,
                vectors_config = VectorParams(size=vector_size,distance=Distance.COSINE,)
            )
            print(f"Created collection: "f"{self.collection_name}")

        else:
            print(f"Collection already exists: "f"{self.collection_name}")

    # --------------------------------------------------
    # Insert chunks
    # --------------------------------------------------
    def add_chunks(self,chunks,embeddings):
        points = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=index,
                vector=embedding.tolist(),
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"],
                    **chunk["metadata"]
                }
            )
            points.append(point)

        self.client.upsert(collection_name=self.collection_name,points=points,)

        print( f"Inserted {len(points)} chunks")

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(self,query_vector,limit=5):
        print(f"Searching for: {query_vector}")
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=limit,
            with_payload=True,
        )

        return results.points