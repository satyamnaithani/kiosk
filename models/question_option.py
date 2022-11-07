from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base

class QuestionOption(Base):
    __tablename__ = "question_options"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    question_id = Column(BigInteger, ForeignKey("training_questions.id"))
    question_option = Column(Unicode(255))
    is_correct = Column(Boolean)

    # question = relationship("TrainingQuestion", back_populates="options")