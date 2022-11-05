from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class QuestionOption(declarative_base()):
    __tablename__ = "question_options"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    question_id = Column(BigInteger)
    question_option = Column(Unicode(255))
    is_correct = Column(Boolean)

    # question = relationship("TrainingQuestion", back_populates="options")