from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text, Boolean
from sqlalchemy.orm import relationship
from config.db import Base

class Department(Base):
    __tablename__ = "departments"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(Unicode(255))
    hod = Column(BigInteger, ForeignKey("employees.id"))
    status = Column(Boolean)
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # employees = relationship("Employee", back_populates="department")