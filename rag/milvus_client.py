from pymilvus import Collection, connections
from sentence_transformers import SentenceTransformer

connections.connect("default", host="localhost", port="19530")
model = SentenceTransformer("all-MiniLM-L6-v2")
collection = Collection("complaint_examples")

class RAGRetriever:
    def search(self, query_text, top_k=3):
        vec = model.encode([query_text])
        results = collection.search(
            vec, anns_field="embedding", param={"metric_type": "L2"}, limit=top_k,
            output_fields=["complaint_text"]
        )
        return [hit.entity.get("complaint_text") for hit in results[0]]
