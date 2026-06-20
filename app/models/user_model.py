from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship  # ← agregar
from datetime import datetime
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)  # ✅ corregido
    created_at = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="user")