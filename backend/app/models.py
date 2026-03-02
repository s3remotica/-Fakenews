from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class AnalysisRecord(Base):
    __tablename__ = 'analysis_records'

    id = Column(Integer, primary_key=True, index=True)
    input_type = Column(String(20), nullable=False)
    input_value = Column(Text, nullable=False)
    label = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=False)
    highlights = Column(Text, nullable=False)
    save_history = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
