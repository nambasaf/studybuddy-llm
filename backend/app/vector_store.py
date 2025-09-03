from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os
from typing import List
import uuid

class VectorStore:
    def __init__(self, index_name: str ="studybuddy-docs", model_name: str = "all-MiniLM-L6-v2"):
        # Initialize Pinecone v6
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = index_name

        # connect to existing index
        self.index = self.pc.Index(self.index_name)

        # embedding model
        self.encoder = SentenceTransformer(model_name)

        # sanity: for ensuring dim matches index
        stats = self.index.describe_index_stats()
        dim = stats.get("dimension")
        if dim != 384: 
            raise ValueError(f"Index dimension={dim} does not match model ({model_name}) dim=384")
        
        def embed_text(self, text: str) -> List[float]:
            """Convert text to embedding"""
            return self.encoder.encode(text).tolist()
        
        def store_chunks(self, chunks: List[str], document_id: str):
            """Store document chunks in vector database"""
            vectors = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id}_{i}"
                embedding = self.embed_text(chunk)

                vectors.append({
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk,
                        "document_id": document_id,
                        "chunk_index": i 
                    }
                })
            # Upload to Pinecone in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
        
        def search_similar(self, query: str, top_k: int = 5) -> List[dict]:
            """Return the top 5 most similar chunks to the query with text + score"""
            query_embedding = self.embed_text(query)
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            return [
                {
                    "text": match["metadata"]["text"], 
                    "score": match["score"]
                }
                for match  in results["matches"]
                
            ]


