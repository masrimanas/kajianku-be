from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, FLOAT
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from app.database import Base


class KajianModel(Base):
    __tablename__ = "kajian"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4)
    title = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=True)
    content = Column(String, nullable=False)
    location = Column(String, nullable=False)
    longlat = Column(ARRAY(FLOAT), nullable=True)
    date = Column(DateTime, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    category_id = Column(Integer, ForeignKey("kajian_category.id"), nullable=False)
    organizers = Column(ARRAY(String), nullable=False)
    speakers = Column(ARRAY(String), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = relationship("KajianCategoryModel", back_populates="kajian")
    author = relationship("UserModel", back_populates="kajian")

    # def __init__(
    #     self,
    #     name,
    #     title,
    #     images,
    #     content,
    #     location,
    #     longlat,
    #     date,
    #     category_id,
    #     organizers,
    #     speakers,
    #     author_id,
    #     author,
    #     category,
    # ):
    #     self.name = name
    #     self.title = title
    #     self.images = images
    #     self.content = content
    #     self.location = location
    #     self.longlat = longlat
    #     self.date = date
    #     self.category_id = category_id
    #     self.organizers = organizers
    #     self.speakers = speakers
    #     self.author_id = author_id
    #     self.author = author
    #     self.category = category

    # def __repr__(self):
    #     return f"<KajianModel {self.title}>"

    # def __str__(self):
    #     return f"<KajianModel {self.title}>"

    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "name": self.name,
    #         "images": self.images,
    #         "content": self.content,
    #         "location": self.location,
    #         "longlat": self.longlat,
    #         "date": self.date,
    #         "category_id": self.category_id,
    #         "organizers": self.organizers,
    #         "speakers": self.speakers,
    #         "author_id": self.author_id,
    #         "author": self.author.to_json(),
    #         "category": self.category.to_json(),
    #     }


class KajianCategoryModel(Base):
    __tablename__ = "kajian_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    kajian = relationship("KajianModel", back_populates="category")

    def __repr__(self):
        return f"<KajianCategoryModel {self.name}>"

    def __str__(self):
        return f"<KajianCategoryModel {self.name}>"

    def to_json(self):
        return {"id": self.id, "name": self.name}
