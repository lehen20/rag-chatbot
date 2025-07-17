import os
import hashlib
import lancedb
from pypdf import PdfReader
import pyarrow as pa
from embedding import embed_model

# Init
docs_folder = "documents" 
db = lancedb.connect("lancedb_data")
table_name = "grievance_docs"

# Schema
schema = pa.schema([
    pa.field("chunk", pa.string(), True),
    pa.field("vector", pa.list_(pa.float32(), 384)),
    pa.field("doc_id", pa.string(), True)
])

# Create table
if table_name not in db.table_names():
    table = db.create_table(table_name, schema=schema, mode="overwrite")
else:
    table = db.open_table(table_name)

# Checking duplicates
def compute_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

existing_ids = set(table.to_pandas()["doc_id"].tolist())

# Embed
for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(docs_folder, filename)
        reader = PdfReader(file_path)
        full_text = "\n".join([page.extract_text() or "" for page in reader.pages])
        if not full_text.strip():
            continue

        doc_hash = compute_hash(full_text)
        if doc_hash in existing_ids:
            print(f"Skipping duplicate: {filename}")
            continue

        # Chunking
        paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]
        for para in paragraphs:
            embedding = embed_model.encode(para).tolist()
            table.add([{"chunk": para, "vector": embedding, "doc_id": doc_hash}])
        print(f"Ingested: {filename}")

