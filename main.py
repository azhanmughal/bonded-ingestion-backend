from fastapi import FastAPI
from ingestion_router import router

app = FastAPI(
    title="Bonded Ingestion API",
    docs_url="/docs"
)

@app.get("/")
def root():
    return {"message": "Backend is working"}


app.include_router(router)
