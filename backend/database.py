from sqlmodel import SQLModel, create_engine,Session
from backend.models import Location, Earthquake, Aftershock

db_path = "C:/Users/melva/OneDrive/Desktop/ASU/IEE305/earthquake-project/earthquake.db"
DATABASE_URL=f"sqlite:///{db_path}"

engine= create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine)as session:
        yield session

if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created.")