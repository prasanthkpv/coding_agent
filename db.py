from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import config

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)
