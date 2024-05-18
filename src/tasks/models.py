import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from src.settings.database import Base


class StatusChoice(enum.Enum):
    done = "done"
    todo = "todo"
    blocked = "blocked"
    doing = "doing"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    status = Column(Enum(StatusChoice), default=StatusChoice.todo)
    project_id = Column(Integer, ForeignKey("project.id"))

    project = relationship("Project", back_populates="tasks")
