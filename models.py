# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    _tablename_ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # relasi ke Contact
    contacts = relationship(
        "Contact",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Contact(Base):
    _tablename_ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # relasi ke User
    user = relationship("User", back_populates="contacts")
