from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.settings.database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="project")
