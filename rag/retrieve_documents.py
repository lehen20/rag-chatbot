from rag.embedding import embed_model
import lancedb

def retrieve_similar_chunks(query: str, top_k: int = 5) -> list:
    
    # Get embedding
    query_embedding = embed_model.encode(query).tolist()

    # Connect to LanceDB and load the table
    db = lancedb.connect(r"rag/lancedb_data")
    table = db.open_table("grievance_docs")

    # Vector similarity search
    results = table.search(query_embedding).limit(top_k).to_pandas()

    return results["chunk"].tolist()
