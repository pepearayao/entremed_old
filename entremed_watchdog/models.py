from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float

class Spiders(Base):
    __tablename__ = 'spiders'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True)
    spider_name = Column(String)
    scheduled_status = Column(String)
    exit_status = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    memusage_startup = Column(Float)
    memusage_max = Column(Float)
    elapsed_time_seconds = Column(Float)
    items_scraped = Column(Integer)
    items_saved = Column(Integer)
    posting_service = Column(String)
 
class Errors(Base):
    __tablename__ = 'errors'
    
    id = Column(Integer, primary_key=True, index=True)
    docker_name = Column(String)
    process_name = Column(String)
    service_ip = Column(String)
    error_type = Column(String)
    pushed_status = Column(Boolean, default=False)
    creation_time = Column(DateTime) 
    spider_name = Column(String)
    posting_service = Column(String)
    error_detail = Column(String)
    http_status_code = Column(Integer)
    website_error = Column(String)

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    error_id = Column(Integer, ForeignKey("errors.id"))
    status = Column(Integer)
    time_sent = Column(DateTime)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)