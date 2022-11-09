from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base

class Grievance(Base):
    __tablename__ = "grievances"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(Unicode(255))
    description = Column(Unicode(255))
    status = Column(Unicode(255))
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(BigInteger, ForeignKey("employees.id"))
    closed_at = Column(DATETIME)
    closed_by = Column(BigInteger, ForeignKey("departments.hod"))
    remarks = Column(Unicode(255))
    grievance_feedback = Column(Unicode(255))

    