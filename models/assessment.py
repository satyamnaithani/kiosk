from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text, Boolean
from sqlalchemy.orm import relationship
from config.db import Base

class Assesment(Base):
    __tablename__ = "employee_assessments"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    employee_id = Column(BigInteger, ForeignKey("employees.id"))
    assessment_id = Column(BigInteger, ForeignKey("employee_assessments.id"))
    training_id = Column(BigInteger, ForeignKey("trainings.id"))
    status = Column(Boolean)
    score = Column(BigInteger)
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
