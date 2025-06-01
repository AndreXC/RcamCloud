from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileHash(Base):
    __tablename__ = "file_hashes"

    id = Column(Integer, primary_key=True)
    filename = Column(Text, unique=True, nullable=False)
    hash = Column(Text, nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.current_timestamp())
