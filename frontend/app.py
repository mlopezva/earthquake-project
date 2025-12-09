import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"  # FastAPI local server

st.title("Earthquake Data Dashboard")

#helper for displaying data
def show_data(data):
    """Safely display data in Streamlit as table"""

    if not data:
        st.write("No results Found.")
        return
        
    if isinstance(data,dict): 
            data = [data]
    if isinstance(data,list): 
            
        if all(not isinstance(item,dict)for item in data):
            data = [{"value":item}for item in data]
        st.dataframe(pd.DataFrame(data))
    else:
        st.dataframe(pd.DataFrame([{"value":data}]))
#Query 1: Earthquakes with Nearby Aftershocks (<50 km)
if st.button("Show Eathquakes with Nearby Aftershock"):
    response=requests.get(f"{BASE_URL}/earthquakes/nearby-aftershocks")
    data=response.json()

    show_data(data)

#Query 2: Top 5 Regions by Average Magnitude
if st.button("Show Top 5 Regions by Average Magnitude"):
    response=requests.get(f"{BASE_URL}/regions/top-5-avg-magnitude")
    data=response.json()

    show_data(data)
    

#Query 3: Strong Aftershocks (>4.0) Within 24 Hours

if st.button("Show Strong Aftershocks(24h)"):
    response = requests.get(f"{BASE_URL}/aftershocks/strong-24h")
    data = response.json()
    show_data(data)

# Query 4: Aftershocks above magnitude 5 with main earthquake info
if st.button("Show Aftershocks (Magnitude > 5)"):
    response = requests.get(f"{BASE_URL}/aftershocks/main-info-magnitude-gt-5")
    data = response.json()
    show_data(data)

# Query 5: Regions above average earthquake counts
if st.button("Regions with Above Average Earthquake Counts"):
    response = requests.get(f"{BASE_URL}/regions/above-average-count")
    data = response.json()
    show_data(data)

# Query 6: Top 10 seismically active regions
if st.button("Top 10 Seismically Active Regions"):
    try:
        response = requests.get(f"{BASE_URL}/regions/top-seismic-activity")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.write(f"Failed to fetch data:{e}")
        data=[]

    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.write("No results found.")
 
 


# Query 7: Earthquakes above overall average magnitude
if st.button("Earthquakes Above Average Magnitude"):
    response = requests.get(f"{BASE_URL}/earthquakes/above-average-magnitude")
    data = response.json()
    show_data(data)
