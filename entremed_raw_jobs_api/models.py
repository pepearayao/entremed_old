from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)

class RawJobsPostings(Base):

    __tablename__ ='raw_job_postings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    source_url = Column(String)
    posting_url = Column(String,unique=True, index=True)
    geolocalization = Column(String)
    company = Column(String)
    salary = Column(String)
    experience = Column(String)
    work_schedule = Column(String)
    shift_type = Column(String)
    employment_type = Column(String)
    slots_avaliable = Column(String)
    urgency_required = Column(Boolean, default=False)
    seniority_level = Column(String)
    driving_level = Column(String)
    posting_service = Column(String)
    description = Column(String)
    requisites = Column(String)
    pills = Column(String)
    inclusive_posting = Column(Boolean, default=False)
    published_date = Column(String)
    closing_date = Column(String)
    scanned_date = Column(String)
    normalized_date = Column(String)
    detailed_scan = Column(Boolean, default=False)
    filtered_posting = Column(Boolean, default=False)
