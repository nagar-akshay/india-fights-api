from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
engine = create_engine('sqlite:///myneta_data.db')
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Define your model
class ConstituencyData(Base):
    __tablename__ = 'constituency_data'
    id = Column(Integer, primary_key=True)
    state_or_ut = Column(String)
    constituency = Column(String)
    href = Column(String)
    candidates = relationship('CandidateData', back_populates='constituency')


class CandidateData(Base):
    __tablename__ = 'candidate_info'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    party = Column(String)
    criminal_cases = Column(Integer)
    education = Column(String)
    age = Column(Integer)
    total_assets = Column(Integer)
    liabilities = Column(Integer)
    winner = Column(Boolean)
    constituency_id = Column(Integer, ForeignKey('constituency_data.id'), nullable=False)
    constituency = relationship('ConstituencyData', back_populates='candidates')

# Create the tables
Base.metadata.create_all(engine)
