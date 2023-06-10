# pylint: disable=invalid-name
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4)
    name = Column(String(50))
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean, nullable=True)

    kajian = relationship("KajianModel", back_populates="author")

    def __init__(self, uuid, name, username, email, password, is_admin):
        self.uuid = uuid
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User {self.name}>"

    def __str__(self):
        return f"<User {self.name}>"

    def to_json(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
        }
