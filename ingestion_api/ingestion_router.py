from fastapi import APIRouter, UploadFile, File, HTTPException
from extract_text import extract_text_from_file
from chunk_text import chunk_text
from generate_embeddings import get_embedding
from insert_to_supabase import insert_embeddings
from datetime import datetime
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        print(f"✅ Received and saved file: {file_path}")

        text = extract_text_from_file(file_path)
        chunks = chunk_text(text)

        records = []
        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            records.append({
                "chunk_index": i,
                "chunk_text": chunk,
                "embedding": emb,
                "document_id": file_id,
                "source_file": file.filename,
                "created_at": datetime.now().isoformat()
            })

        insert_embeddings(records)
        return {"status": "success", "chunks_ingested": len(records), "document_id": file_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
