from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Test API OK"}

@app.get("/health")
def health():
    return {"status": "healthy"}