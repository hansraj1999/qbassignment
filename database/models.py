from database.database import Base
from sqlalchemy import Column, Integer, String


class Student(Base):
    __tablename__ = "Student"
    name = Column(String(50))
    email = Column(String(50), primary_key=True)
    password = Column(String(50))
    president_voted_for_id = Column(Integer, nullable=True)
    president_voted_for_name = Column(String(50), nullable=True)
    vice_president_voted_for_id = Column(Integer, nullable=True)
    vice_president_voted_for_name = Column(String(50), nullable=True)


class President(Base):
    __tablename__ = "President"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    total_votes = Column(Integer, server_default='0', nullable=False)


class VicePresident(Base):
    __tablename__ = "VicePresident"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    total_votes = Column(Integer, nullable=False, server_default='0')


