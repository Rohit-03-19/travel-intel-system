from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# SQLite local file path
DB_URL = "sqlite:///./travel_intel.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Step 4: Design the Table Model ---
class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    destination = Column(String, nullable=False)
    final_plan = Column(JSON, nullable=True) # JSON store karega
    reality_report = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Step 5: Create Table Automatically ---
def init_db():
    Base.metadata.create_all(bind=engine)

# --- Step 6: Save Data Function ---
def save_trip(query, dest, plan, report):
    db = SessionLocal()
    try:
        new_trip = Trip(
            user_query=query,
            destination=dest,
            final_plan=plan,
            reality_report=report
        )
        db.add(new_trip)
        db.commit()
        db.refresh(new_trip)
        return new_trip.id
    finally:
        db.close()
        
def get_all_trips():
    db = SessionLocal()
    try:
        # Saari trips return karega (Latest first)
        return db.query(Trip).order_by(Trip.id.desc()).all()
    finally:
        db.close()

def get_trip_by_id(trip_id: int):
    db = SessionLocal()
    try:
        return db.query(Trip).filter(Trip.id == trip_id).first()
    finally:
        db.close()