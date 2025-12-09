import os
from sqlmodel import SQLModel, create_engine, Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_folder = os.path.join(BASE_DIR, "database")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "earthquake.db")

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

if __name__ == "__main__":
    create_db_and_tables()
    print(f"Database created at: {db_path}")
