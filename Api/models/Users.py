from sqlalchemy import Column,String,Enum,Integer,Boolean,TIMESTAMP
from Api.models.base_class import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from Api.models.Transaction import Transaction


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(30), primary_key=True)
    full_name = Column(String(80))
    mail = Column(String(100), unique=True)
    passhash = Column(String(140))
    user_role = Column(Enum('admin','user'))
    user_status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")

