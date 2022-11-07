from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base

class TrainingQuestion(Base):
    __tablename__ = "training_questions"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    training_id = Column(BigInteger, ForeignKey("trainings.id"))
    question = Column(Unicode(255))
    score = Column(Unicode(255))
    status = Column(Boolean)
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    options = relationship("QuestionOption")
    training = relationship("Training", back_populates="training_questions")
