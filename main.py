from fastapi import FastAPI
from .ingestion_router import router

app = FastAPI()
app.include_router(router)
