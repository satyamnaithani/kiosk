from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base

class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    question_id = Column(BigInteger, ForeignKey("training_questions.id"))
    answer_id = Column(BigInteger, ForeignKey("question_options.id"))
    employee_id = Column(BigInteger, ForeignKey("employees.id"))
    assessment_id = Column(BigInteger, ForeignKey("employee_assessments.id"))

    question = relationship("TrainingQuestion")
