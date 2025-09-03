# test_pinecone.py (fixed)
from dotenv import load_dotenv
import os, time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = "studybuddy-docs"
index = pc.Index(INDEX_NAME)

print("Your indexes:", [i.name for i in pc.list_indexes()])
print("Index stats BEFORE:", index.describe_index_stats())

# Embed
encoder = SentenceTransformer("all-MiniLM-L6-v2")
text = "This is a test document about machine learning."
vec = encoder.encode(text).tolist()
print("Embedding dimension:", len(vec))  # should be 384

# Upsert (note the keyword `vectors=`)
index.upsert(
    vectors=[{"id": "test-1", "values": vec, "metadata": {"text": text}}]
)

# tiny wait (serverless is usually instant, but 0.3s avoids race conditions)
time.sleep(0.3)

print("Index stats AFTER:", index.describe_index_stats())

# Query it back
res = index.query(vector=vec, top_k=1, include_metadata=True)
if res.get("matches"):
    top = res["matches"][0]
    print("Top match text:", top["metadata"]["text"])
    print("Score:", top["score"])
else:
    print("No matches returned. (Check upsert, index name, and vector dimension.)")
