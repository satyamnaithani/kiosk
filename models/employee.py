from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Unicode, BigInteger, DATETIME, text
from sqlalchemy.ext.declarative import declarative_base

class Employee(declarative_base()):
    __tablename__ = "employees"

    id: Unicode = Column(BigInteger, primary_key=True, nullable=False)
    employee_code = Column(Unicode(255))
    name = Column(Unicode(255))
    department_id = Column(BigInteger)
    mobile = Column(Unicode(255))
    email = Column(Unicode(255))
    password = Column(Unicode(255))
    type = Column(Unicode(255))  
    created_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DATETIME, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # department = relationship("Department", back_populates="employees")