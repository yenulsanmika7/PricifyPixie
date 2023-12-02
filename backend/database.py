from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./pricewise_tacker.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class TrackedProducts(Base):
    __tablename__ = "tracked-products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1000))
    email = Column(String(1000))
    url = Column(String(1000))
    price = Column(Float)
    image = Column(String(3000))
    created_at = Column(DateTime, default=func.now())
    tracked = Column(Boolean, default=True)
    
Base.metadata.create_all(bind=engine)  # This line creates the tables

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(bind=engine)