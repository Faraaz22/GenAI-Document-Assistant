from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.sql import func


class Document(Base):
    __tablename__  = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(300))
    summary = Column(Text)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())

class QuestionLog(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    question = Column(Text)
    answer = Column(Text)
    justification = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)