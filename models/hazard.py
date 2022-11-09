from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db import Base

class Hazard(Base):
    __tablename__ = "hazards"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(Unicode(255))
    description = Column(Unicode(255))
    type = Column(Unicode(255))
    department_id = Column(BigInteger, ForeignKey("departments.id"))
    status = Column(Unicode(255))
    created_by = Column(BigInteger, ForeignKey("employees.id"))
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    closed_at = Column(DATETIME)
    closed_by = Column(BigInteger, ForeignKey("departments.hod"))
    remarks = Column(Unicode(255))
    hazard_feedback = Column(Unicode(255))

    