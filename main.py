from fastapi import FastAPI
from backend.queries import (
    earthquakes_with_nearby_aftershocks,
    top_5_regions_by_avg_magnitude,
    strong_aftershocks_within_24h,
    aftershocks_main_info_magnitude_gt_5,
    regions_above_avg_earthquake_counts,
    top_10_seismically_active_regions,
    earthquakes_above_average_magnitude
)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Earthquake API running"}

@app.get("/earthquakes/nearby-aftershocks")
def get_earthquakes_with_nearby_aftershocks():
    return earthquakes_with_nearby_aftershocks()

@app.get("/regions/top-avg-magnitude")
def get_top_5_regions_by_avg_magnitude():
    return top_5_regions_by_avg_magnitude()

@app.get("/aftershocks/strong-24h")
def get_strong_aftershocks_within_24h():
    return strong_aftershocks_within_24h()

@app.get("/aftershocks/main-info-magnitude-gt-5")
def get_aftershocks_main_info_magnitude_gt_5():
    return aftershocks_main_info_magnitude_gt_5()

@app.get("/regions/above-average-count")
def get_regions_above_avg_earthquake_counts():
    return regions_above_avg_earthquake_counts()

@app.get("/regions/top-seismic-activity")
def get_top_10_seismically_active_regions():
    return top_10_seismically_active_regions()

@app.get("/earthquakes/above-average-magnitude")
def get_earthquakes_above_average_magnitude():
    return earthquakes_above_average_magnitude()

@app.get("/earthquakes/with-aftershocks-region")
def query_8():
    return earthquakes_with_aftershocks_and_region()

@app.get("/earthquakes/aftershock-counts")
def query_9():
    return aftershock_counts_per_earthquake()

@app.get("/earthquakes/above-threshold")
def query_10(min_magnitude: float = 4.0):
    return earthquakes_above_threshold(min_magnitude)
