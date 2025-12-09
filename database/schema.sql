-- Table Location
CREATE TABLE location (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL,
    risk_level TEXT,
    region_population INTEGER
);

-- Table Earthquake
CREATE TABLE earthquake (
    earthquake_id TEXT PRIMARY KEY,
    location_id INTEGER,
    magnitude REAL NOT NULL,
    event_time TEXT NOT NULL,
    event_duration REAL,
    latitude REAL,
    longitude REAL,
    depth REAL,
    place TEXT NOT NULL,
    FOREIGN KEY(location_id) REFERENCES location(location_id)
);

-- Table Aftershock
CREATE TABLE aftershock (
    aftershock_id TEXT PRIMARY KEY,
    earthquake_id TEXT NOT NULL,
    magnitude REAL NOT NULL,
    distance_from_main REAL,
    event_time TEXT NOT NULL,
    event_duration REAL,
    FOREIGN KEY(earthquake_id) REFERENCES earthquake(earthquake_id)
);
