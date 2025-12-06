from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import Optional, List
from datetime import datetime

class Location(SQLModel, table=True):
    location_id: Optional[int]=Field(default= None, primary_key=True)
    region_name:str
    risk_level:Optional[str]= None
    region_population: Optional[int]= None
    earthquakes: List["Earthquake"]=Relationship(back_populates="location")

class Earthquake(SQLModel, table=True):
    earthquake_id:str =Field(primary_key=True) #USGS uses id as strings
    location_id:int=Field(default=None, foreign_key="location.location_id")
    magnitude:float
    event_time:datetime
    event_duration:Optional[float]= None
    latitude:Optional[float]= Field(default=None)
    longitude:Optional[float]=Field(default=None)
    depth:Optional[float]=Field(default=None)
    place:str

    location:Optional[Location] = Relationship(back_populates="earthquakes")
    aftershocks:List["Aftershock"]=Relationship(back_populates="earthquake")

class Aftershock(SQLModel, table=True):
    aftershock_id: str = Field(primary_key=True)
    earthquake_id:str= Field(foreign_key="earthquake.earthquake_id")
    magnitude:float
    distance_from_main:Optional[float]=None
    event_time:datetime
    event_duration:Optional[float]=None
    earthquake:Optional[Earthquake] = Relationship(back_populates="aftershocks")
