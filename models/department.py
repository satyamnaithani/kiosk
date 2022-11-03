from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class Department(declarative_base()):
    __tablename__ = "departments"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(Unicode(255))
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    employees = relationship("Employee", back_populates="department")