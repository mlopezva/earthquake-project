import requests
from datetime import datetime, timedelta
from sqlmodel import Session, select
from backend.models import Location, Earthquake, Aftershock
from backend.database import engine, create_db_and_tables

# Create database and tables if not exist
create_db_and_tables()

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_earthquake_data():
    # Use a smaller date range for testing
    endtime = datetime.utcnow().strftime("%Y-%m-%d")
    starttime = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")

    params = {
        "format": "geojson",
        "minmagnitude": 1.0,
        "limit": 50,
        "starttime": starttime,
        "endtime": endtime
    }

    # Fetch data with error handling
    try:
        response = requests.get(USGS_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return {"status": "Failed to fetch data"}
    except ValueError as e:
        print("Failed to parse JSON:", e)
        return {"status": "Failed to parse data"}

    features = data.get("features", [])
    print(f"Found {len(features)} earthquakes")

    with Session(engine) as session:
        for feature in features:
            props = feature.get("properties", {})
            geo = feature.get("geometry", {}).get("coordinates", [])
            longitude = geo[0] if len(geo)> 0 else None
            latitude= geo[1] if len(geo)> 1 else None
            depth= geo[2] if len(geo)> 2 else None
            region_name = props.get("place", "Unknown")

            # Location
            location = session.exec(
                select(Location).where(Location.region_name == region_name)
            ).first()
            if not location:
                location = Location(
                    region_name=region_name,
                    risk_level="Unknown",
                    region_population=None
                )
                session.add(location)
                session.flush()
                   

            # Earthquake
            eq_id = feature.get("id")
            magnitude=props.get("mag")
            if not eq_id or magnitude is None:
                continue

            earthquake = session.get(Earthquake, eq_id)
            if not earthquake:
                earthquake = Earthquake(
                    earthquake_id=eq_id,
                    location_id=location.location_id,
                    magnitude=magnitude,
                    event_time=datetime.fromtimestamp(props["time"]/1000),
                    event_duration=60.0,
                    latitude=latitude,
                    longitude=longitude,
                    depth=depth,
                    place=region_name
                )
                session.add(earthquake)
               
               
                print(f"Inserted earthquake {eq_id}")

            # Aftershock
            aftershock_id = f"{eq_id}_a"
            existing_aftershock = session.get(Aftershock, aftershock_id)
            if not existing_aftershock:
                aftershock = Aftershock(
                    aftershock_id=aftershock_id,
                    earthquake_id=earthquake.earthquake_id,
                    magnitude=max(0.1, props["mag"] - 1.0),
                    distance_from_main=10.0,
                    event_time=datetime.fromtimestamp(props["time"]/1000),
                    event_duration=30
                )
                session.add(aftershock)
               
                print(f"Inserted aftershock {aftershock_id}")
    session.commit()
    print("Data insertion complete")
    return {"status": "Data inserted successfully"}


if __name__ == "__main__":
    fetch_earthquake_data()
