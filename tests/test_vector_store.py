from embeddings.embedder import CodeEmbedder
from vector_store.qdrant_store import QdrantStore

# ==================================================
# 1. Sample code chunks
# ==================================================
chunks = [
    {
        "chunk_id": "auth.py::function::0",

        "content": """
            def authenticate(token):
                user = verify_token(token)
                return user
                """,

        "metadata": {
            "file_path": "auth.py",
            "language": "python",
            "type": "function",
            "name": "authenticate",
            "start_line": 1,
            "end_line": 3,
        }
    },

    {
        "chunk_id": "redis.py::function::0",

        "content": """
            def connect_redis():
                return redis.Redis(
                    host="localhost"
                    )
                """,

        "metadata": {
            "file_path": "redis.py",
            "language": "python",
            "type": "function",
            "name": "connect_redis",
            "start_line": 1,
            "end_line": 4,
        }
    },

    {
        "chunk_id": "math.py::function::0",

        "content": """
                def fibonacci(n):
                    if n <= 1:
                        return n
                    return fibonacci(n - 1) + fibonacci(n - 2)
                """,

        "metadata": {
            "file_path": "math.py",
            "language": "python",
            "type": "function",
            "name": "fibonacci",
            "start_line": 1,
            "end_line": 7,
        }
    }
]

# ==================================================
# 2. Create embedding model
# ==================================================
print("Loading embedding model...")
embedder = CodeEmbedder()

# ==================================================
# 3. Generate embeddings for code chunks
# ==================================================
texts = [
    chunk["content"]
    for chunk in chunks
]

embeddings = embedder.embed(texts)


print("Embedding dimension:",len(embeddings[0]))

# ==================================================
# 4. Connect to Qdrant Cloud
# ==================================================
print("Connecting to Qdrant Cloud...")

store = QdrantStore(collection_name="codebase")


# ==================================================
# 5. Create collection
# ==================================================

store.create_collection(vector_size=len(embeddings[0]))


# ==================================================
# 6. Store chunks
# ==================================================

store.add_chunks(chunks,embeddings)

# ==================================================
# 7. Create query
# ==================================================
query = (
    "Where is user authentication "
    "implemented?"
)


# ==================================================
# 8. Embed query
# ==================================================

query_vector = embedder.embed([query])[0]

# ==================================================
# 9. Search Qdrant
# ==================================================

results = store.search(query_vector=query_vector,limit=3)

# ==================================================
# 10. Display results
# ==================================================
print()
print("=" * 70)
print("SEARCH RESULTS")
print("=" * 70)


for result in results:
    print()
    print("Score:",result.score)
    print("Chunk ID:",result.payload["chunk_id"])
    print("File:",result.payload["file_path"])
    print("Name:",result.payload["name"])
    print("Type:",result.payload["type"])
    print("Lines:",result.payload["start_line"],"-",result.payload["end_line"])
    print()
    print(result.payload["content"])
    print("-" * 70)