from backend.database import engine
from backend.models import Earthquake, Aftershock, Location
from sqlmodel import Session, select
from datetime import timedelta

def earthquakes_with_nearby_aftershocks():
    with Session(engine) as session:
        stmt = (
            select(Earthquake, Aftershock)
            .join(Aftershock, Earthquake.earthquake_id == Aftershock.earthquake_id)
            .where(Aftershock.distance_from_main <= 50)
        )
        rows = session.exec(stmt).all()

        return [
            {
                "earthquake_id": e.earthquake_id,
                "magnitude": e.magnitude,
                "aftershock_id": a.aftershock_id,
                "aftershock_magnitude": a.magnitude,
            }
            for e, a in rows
        ]


def top_5_regions_by_avg_magnitude():
    with Session(engine) as session:
        locations = session.exec(select(Location)).all()
        results = []

        for loc in locations:
            earthquakes = loc.earthquakes or []
            avg_mag = (
                sum(e.magnitude for e in earthquakes) / len(earthquakes)
                if earthquakes else 0
            )
            results.append({
                "region": loc.region_name,
                "avg_magnitude": round(avg_mag, 3),
            })

        results.sort(key=lambda x: x["avg_magnitude"], reverse=True)
        return results[:5]


def strong_aftershocks_within_24h():
    with Session(engine) as session:
        stmt = (
            select(Aftershock, Earthquake)
            .join(Earthquake, Aftershock.earthquake_id == Earthquake.earthquake_id)
        )

        rows = session.exec(stmt).all()

        results = []
        for a, e in rows:
            if a.magnitude > 4:
                if e.event_time <= a.event_time <= e.event_time + timedelta(hours=24):
                    results.append({
                        "aftershock_id": a.aftershock_id,
                        "magnitude": a.magnitude,
                        "earthquake_id": e.earthquake_id,
                        "event_time": a.event_time,
                    })
        return results
