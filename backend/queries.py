from backend.database import engine
from backend.models import Earthquake, Aftershock, Location
from sqlmodel import Session, select
from datetime import timedelta

def earthquakes_with_nearby_aftershocks():
    with Session(engine) as session:
        statement = (
            select(Earthquake,Aftershock)
            .join(Aftershock,Earthquake.earthquake_id == Aftershock.earthquake_id)
            .where(Aftershock.distance_from_main<=50)
        )
        results = session.exec(statement).all()
        return results
    
def top_5_regions_by_avg_magnitude():
     with Session(engine) as session:
        locations = session.exec(select(Location)).all()  
        results = []
        for loc in locations:
            earthquakes = loc.earthquakes if loc.earthquakes else []
            avg_mag = sum(e.magnitude for e in earthquakes) / len(earthquakes) if earthquakes else 0
            results.append({"region": loc.region_name, "avg_magnitude": avg_mag})
    
        results.sort(key=lambda x: x["avg_magnitude"], reverse=True)
        return results[:5]
     
def strong_aftershocks_within_24h():
    with Session(engine) as session:
      aftershocks = session.exec(select(Aftershock)).all()
      results = []

    for a in aftershocks:
            if a.magnitude > 4 and a.earthquake:
                eq_time = a.earthquake.event_time
                if eq_time <= a.event_time <= eq_time + timedelta(hours=24):
                    results.append({
                        "aftershock_id": a.aftershock_id,
                        "magnitude": a.magnitude,
                        "earthquake_id": a.earthquake.earthquake_id,
                        "event_time": a.event_time
                    })
    return results
    
if __name__ == "__main__":
    print("Query 1 :", earthquakes_with_nearby_aftershocks())
    print("Query 2:", top_5_regions_by_avg_magnitude())
    print("Query 3:",strong_aftershocks_within_24h())