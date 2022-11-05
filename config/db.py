from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def get_session() -> Session:
    db_connection = "mysql+pymysql://sql12530348:u7PtD9QvYv@sql12.freemysqlhosting.net/sql12530348"
    engine = create_engine(
        db_connection, echo=True, connect_args={"connect_timeout": 10}
    )
    Base.metadata.create_all(bind=engine)
    session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_Local()


# Dependency
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
