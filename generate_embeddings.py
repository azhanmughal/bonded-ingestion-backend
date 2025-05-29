import os
from dotenv import load_dotenv
import openai
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Embedding model to use
EMBEDDING_MODEL = "text-embedding-3-small"

def get_embedding(text: str) -> list[float]:
    try:
        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return None
