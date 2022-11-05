from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class Training(declarative_base()):
    __tablename__ = "trainings"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(Unicode(255))
    description = Column(Unicode(255))
    status = Column(Boolean)
    min_pass_marks = Column(Unicode(255))
    
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # training_questions = relationship("TrainingQuestions", back_populates="question")