from sqlalchemy import Column, Integer, String, Float
from database import Base

class SessionData(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    stress_level = Column(Float)
    focus_score = Column(Float)
    adaptive_score = Column(Float)
    recommendation = Column(String)

