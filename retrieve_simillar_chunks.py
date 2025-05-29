import os
import psycopg2
import openai
from dotenv import load_dotenv

load_dotenv()

# Load credentials
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

# Step 1: Embed the query
def embed_query(query: str) -> list[float]:
    response = openai.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

# Step 2: Search similar chunks in DB
def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    vector = embed_query(query)
    
    conn = psycopg2.connect(SUPABASE_DB_URL)
    cur = conn.cursor()
    
    # Convert vector to PostgreSQL array format
    pg_vector = f"ARRAY{vector}".replace('[', '(').replace(']', ')')
    
    cur.execute(f"""
        SELECT chunk_index, chunk_text, document_id,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY similarity DESC
        LIMIT %s
    """, (vector, top_k))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {
            "chunk_index": row[0],
            "chunk_text": row[1],
            "document_id": row[2],
            "similarity": row[3]
        }
        for row in rows
    ]
