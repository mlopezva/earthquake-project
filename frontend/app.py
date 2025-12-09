import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"  # FastAPI local server

st.title("Earthquake Data Dashboard")

# Query 4: Aftershocks above magnitude 5 with main earthquake info
if st.button("Show Aftershocks (Magnitude > 5)"):
    response = requests.get(f"{BASE_URL}/aftershocks/main-info-magnitude-gt-5")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")

# Query 5: Regions above average earthquake counts
if st.button("Regions with Above Average Earthquake Counts"):
    response = requests.get(f"{BASE_URL}/regions/above-average-count")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")

# Query 6: Top 10 seismically active regions
if st.button("Top 10 Seismically Active Regions"):
    response = requests.get(f"{BASE_URL}/regions/top-seismic-activity")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")

# Query 7: Earthquakes above overall average magnitude
if st.button("Earthquakes Above Average Magnitude"):
    response = requests.get(f"{BASE_URL}/earthquakes/above-average-magnitude")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")

# Query 8: Earthquakes with aftershocks and region info
if st.button("Show Earthquakes With Aftershocks + Region"):
    response = requests.get(f"{BASE_URL}/earthquakes/with-aftershocks-region")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")

# Query 9: Aftershock counts per earthquake
if st.button("Show Aftershock Counts Per Earthquake"):
    response = requests.get(f"{BASE_URL}/earthquakes/aftershock-counts")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")
# Query 10: Earthquakes above a user-selected magnitude
min_mag = st.number_input("Minimum Magnitude", min_value=0.0, max_value=10.0, step=0.1)

if st.button("Find Earthquakes Above Threshold"):
    response = requests.get(f"{BASE_URL}/earthquakes/above-threshold?min_magnitude={min_mag}")
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No results found")
