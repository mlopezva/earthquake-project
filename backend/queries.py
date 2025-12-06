from backend.database import engine
from backend.models import Earthquake, Aftershock, Location
from sqlmodel import Session, select, func
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

def aftershocks_main_info_magnitude_gt_5():
    """Query 4: Aftershocks with main earthquake info and region name above magnitude 5"""
    with Session(engine) as session:
        # Select aftershock, main earthquake, and the region information
        stmt = (
            select(Aftershock, Earthquake, Location)
            .join(Earthquake, Aftershock.earthquake_id == Earthquake.earthquake_id)
            .join(Location, Earthquake.location_id == Location.location_id)
            .where(Earthquake.magnitude > 5) #Above  magnitude of 5
        )
        rows = session.exec(stmt).all()

        # Construct the result as a list of dictionaries
        return [
            {
                "aftershock_id": a.aftershock_id,
                "aftershock_magnitude": a.magnitude,
                "earthquake_id": e.earthquake_id,
                "earthquake_magnitude": e.magnitude,
                "region_name": l.region_name
            }
            for a, e, l in rows
        ]


def regions_above_avg_earthquake_counts():
    """Query 5: Regions with above-average earthquake counts"""
    with Session(engine) as session:
        # Count earthquakes per region
        stmt = select(
            Location.region_name,
            func.count(Earthquake.earthquake_id).label("quake_count")
        ).join(Earthquake, Location.location_id == Earthquake.location_id)\
         .group_by(Location.region_name)

        rows = session.exec(stmt).all()

        # Compute the average count
        if not rows:
            return []

        avg_count = sum(r.quake_count for r in rows) / len(rows)

        # Return only regions with count above average
        return [
            {"region": r.region_name, "count": r.quake_count}
            for r in rows if r.quake_count > avg_count
        ]

def top_10_seismically_active_regions():
    """Query 6: Top 10 most seismically active regions"""
    with Session(engine) as session:
        # Select all locations and their earthquakes
        stmt = select(Location, Earthquake).join(Earthquake, Location.location_id == Earthquake.location_id)
        rows = session.exec(stmt).all()

        # Count earthquakes for each region
        counts = {}
        for loc, eq in rows:
            counts[loc.region_name] = counts.get(loc.region_name, 0) + 1

        # Sort by count descending and return top 10
        sorted_regions = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [{"region": region, "earthquake_count": count} for region, count in sorted_regions[:10]]


def earthquakes_above_average_magnitude():
    """Query 7: Earthquakes with magnitude above overall average"""
    with Session(engine) as session:
        # Get all earthquakes
        all_eq = session.exec(select(Earthquake)).all()
        if not all_eq:
            return []

        # Calculate overall average magnitude
        avg_mag = sum(e.magnitude for e in all_eq) / len(all_eq)
        # Filter earthquakes that have magnitude above the overall average
        above_avg = [e for e in all_eq if e.magnitude > avg_mag]

        # Construct the result as a list of dictionaries
        return [
            {
                "earthquake_id": e.earthquake_id,
                "magnitude": e.magnitude,
                "location_id": e.location_id,
                "event_time": e.event_time
            }
            for e in above_avg
        ]
