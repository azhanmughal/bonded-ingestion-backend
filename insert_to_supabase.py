import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

def insert_embeddings(embedding_records: list[dict]):
    conn = psycopg2.connect(SUPABASE_DB_URL)
    cur = conn.cursor()

    for record in embedding_records:
        try:
            cur.execute(
                """
                INSERT INTO documents (document_id, chunk_index, chunk_text, embedding, source_file, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    record["document_id"],
                    record["chunk_index"],
                    record["chunk_text"],
                    record["embedding"],
                    record["source_file"],
                    record["created_at"]
                )
            )
            print(f"✅ Inserted chunk {record['chunk_index']}")  # Debug print

        except Exception as e:
            print(f"❌ Failed to insert chunk {record['chunk_index']}: {e}")

    conn.commit()
    cur.close()
    conn.close()
