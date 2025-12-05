import requests
from datetime import datetime
from sqlmodel import Session, select
from .models import Location, Earthquake, Aftershock
from .database import engine, create_db_and_tables

create_db_and_tables()

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def fetch_earthquake_data():
    endtime = datetime.utcnow().strftime("%Y-%m-%d")

    params = {
        "format": "geojson",
        "minmagnitude": 1.0,
        "limit": 50,
        "starttime": "2000-01-01",
        "endtime": endtime
    }

    response = requests.get(USGS_URL, params=params)
    data = response.json()

    with Session(engine) as session:
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            geo = feature.get("geometry", {}).get("coordinates", [None, None, None])
            longitude, latitude, depth = geo[0], geo[1], geo[2]

            region_name = props.get("place", "Unknown")

            
            location = session.exec(
                Location.select().where(Location.region_name == region_name)
            ).first()
            if not location:
                location = Location(
                    region_name=region_name,
                    risk_level="Unknown",
                    region_population=None
                )
                session.add(location)
                session.commit()
                session.refresh(location)

            
            eq_id = feature.get("id")
            if not eq_id or props.get("mag") is None:
                continue

            
            earthquake = session.get(Earthquake, eq_id)
            if not earthquake:
                earthquake = Earthquake(
                    earthquake_id=eq_id,
                    location_id=location.location_id,
                    magnitude=props["mag"],
                    event_time=datetime.fromtimestamp(props["time"]/1000),
                    event_duration=60.0,
                    latitude=latitude,
                    longitude=longitude,
                    depth=depth,
                    place=region_name
                )
                session.add(earthquake)
                session.commit()
                session.refresh(earthquake)

            
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
                session.commit()

    return {"status": "Data inserted successfully"}


if __name__ == "__main__":
    print(fetch_earthquake_data())
