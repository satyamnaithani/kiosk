from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from config.db import Base
class Employee(Base):
    __tablename__ = "employees"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    employee_code = Column(Unicode(255))
    name = Column(Unicode(255))
    department_id = Column(BigInteger, ForeignKey("departments.id"))
    mobile = Column(Unicode(255))
    email = Column(Unicode(255))
    password = Column(Unicode(255))
    type = Column(Unicode(255))  
    is_hod = Column(Boolean)
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    department = relationship("Department", foreign_keys=[department_id])