from fastapi import FastAPI
from backend.queries import (earthquakes_with_nearby_aftershocks,top_5_regions_by_avg_magnitude,strong_aftershocks_within_24h)

app = FastAPI()

@app.get("/")
def home():
    return{"message":"Earthquake API running"}

@app.get("/query1")
def query1():
     return  earthquakes_with_nearby_aftershocks()

@app.get("/query2")
def query2():
     return top_5_regions_by_avg_magnitude()

@app.get("/query3")
def query3():
     return  strong_aftershocks_within_24h()
