from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text
from sqlalchemy.orm import relationship
from config.db import Base

class TrainingAssignee(Base):
    __tablename__ = "training_assignees"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    training_id = Column(BigInteger, ForeignKey("trainings.id"))
    employee_id = Column(BigInteger, ForeignKey("employees.id"))
    assigned_on = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    