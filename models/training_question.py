from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class TrainingQuestion(declarative_base()):
    __tablename__ = "training_questions"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    training_id = Column(BigInteger)
    question = Column(Unicode(255))
    score = Column(Unicode(255))
    status = Column(Boolean)
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # options = relationship("QuestionOption", back_populates="question")
    # training = relationship("Training", back_populates="training_questions")