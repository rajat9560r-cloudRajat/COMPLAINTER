from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from .database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer,primary_key=True, nullable=False )
    name = Column(String, nullable=False)
    title = Column(String, nullable=False )
    content = Column(String, nullable=False)
    status = Column(String, nullable=False, server_default="Pending")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())