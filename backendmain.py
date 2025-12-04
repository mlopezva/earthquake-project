from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"message":"Earthquake API running"}