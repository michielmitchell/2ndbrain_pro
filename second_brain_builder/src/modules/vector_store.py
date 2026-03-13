# filename: second_brain_builder/src/modules/vector_store.py
# purpose: ChromaDB wrapper - semantic index only (parallel to .md files, no UI changes)

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pathlib import Path
import hashlib
from src.config import VAULT_ROOT, OLLAMA_HOST

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(VAULT_ROOT / "vector_index"))
        self.embedding_fn = OllamaEmbeddingFunction(
            model_name="nomic-embed-text:latest",
            url=OLLAMA_HOST
        )
        self.collection = self.client.get_or_create_collection(
            name="thoughts",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def embed_thought(self, thought: str, path: str, category: str = "Review", confidence: float = 0.0, datetime_str: str = ""):
        try:
            doc_id = hashlib.md5(path.encode()).hexdigest()
            self.collection.upsert(
                ids=[doc_id],
                documents=[thought],
                metadatas=[{
                    "path": path,
                    "category": category,
                    "confidence": confidence,
                    "datetime": datetime_str
                }]
            )
        except Exception as e:
            print(f"[VECTOR STORE] Embed failed for {path}: {e}")

    def semantic_search(self, query: str, top_k: int = 20, category_filter: str = None):
        try:
            where = {"category": category_filter} if category_filter and category_filter != "all" else None
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where
            )
            hits = []
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                hits.append({
                    "path": meta["path"],
                    "thought": doc[:120] + ("..." if len(doc) > 120 else ""),
                    "category": meta["category"],
                    "confidence": str(meta["confidence"]),
                    "datetime": meta["datetime"]
                })
            return hits
        except Exception as e:
            print(f"[VECTOR STORE] Semantic search failed: {e}")
            return []

vector_store = VectorStore()
