import os
import hashlib
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

    def create_collection(self,vector_size):
        collections = self.client.get_collections()
        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_collections:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                )
            )

            print(f"Created collection: "f"{self.collection_name}")

        else:
            print(f"Collection already exists: "f"{self.collection_name}")

    def add_chunks(self,chunks,embeddings,batch_size=100):
        total_chunks = len(chunks)
        for start in range(0,total_chunks,batch_size):
            end = min(start + batch_size,total_chunks)
            batch_chunks = chunks[start:end]
            batch_embeddings = embeddings[start:end]

            points = []

            for chunk, embedding in zip(batch_chunks,batch_embeddings):
                point_id = int(hashlib.md5(chunk["chunk_id"].encode("utf-8")).hexdigest()[:16],16)

                point = PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload={
                        "chunk_id": chunk["chunk_id"],
                        "content": chunk["content"],
                        **chunk["metadata"]
                    }
                )

                points.append(point)

            self.client.upsert(collection_name=self.collection_name,points=points,)

            print(f"Uploaded chunks "f"{start + 1}-{end} "f"of {total_chunks}")

        print(f"Successfully uploaded "f"{total_chunks} chunks")

    def search(self,query_vector,limit=5):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=limit,
            with_payload=True,
        )

        return results.points