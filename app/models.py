from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey
from .database import Base

class Complaint(Base):
    __tablename__ = "complaints"
 
    id = Column(Integer,primary_key=True, nullable=False )
    name = Column(String, nullable=False)
    title = Column(String, nullable=False )
    content = Column(String, nullable=False)
    status = Column(String, nullable=False, server_default="Pending")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users2.id",ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__ = "users2"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())