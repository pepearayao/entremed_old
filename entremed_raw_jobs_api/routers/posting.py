from typing import Annotated, Optional, Union
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status
from models import RawJobsPostings
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/jobs',
    tags=['jobs']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class RawJobPostingRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    source_url: str = Field(min_length=3)
    posting_url: str = Field(min_length=3)
    geolocalization: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    work_schedule: Optional[str] = None
    shift_type: Optional[str] = None
    employment_type: Optional[str] = None
    slots_avaliable: Optional[str] = None
    urgency_required: Optional[bool] = None
    seniority_level: Optional[str] = None
    driving_level: Optional[str] = None
    posting_service: Optional[str] = None
    description: Optional[str] = None
    requisites: Optional[str] = None
    pills: Optional[str] = None
    inclusive_posting: Optional[bool] = None
    published_date: Optional[str] = None
    closing_date: Optional[str] = None
    scanned_date: Optional[str] = None
    normalized_date: Optional[str] = None
    detailed_scan: Optional[bool] = None
    filtered_posting: Optional[bool] = None

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'The title of the Job Posting',
                'source_url': 'https://trabajando.com/busqueda?enfermeria',
                'posting_url': 'https://trabajando.com/trabajo/2421234234',
                'geolocalization': 'Buin, Región Metropolitana',
                'company': 'Hospital de Buín',
                'salary': '12000000',
                'experience': 'No exige',
                'work_schedule': 'Part-Time',
                'shift_type': '4to turno',
                'employment_type': 'A honorarios',
                'slots_available': '2',
                'urgency_required': False,
                'seniority_level': 'Práctica',
                'driving_level': '',
                'posting_service': 'Trabajando',
                'description': 'Se requiere enfermera de práctica',
                'requisites': 'Titulada',
                'pills': 'full-time | 4o turno | 400.000',
                'inclusive_posting': False,
                'published_date': 'hace 2 días',
                'closing_date': '',
                'scanned_date': '2023-11-23 18:54:33:3455322',
                'normalized_date': '',
                'detailed_scan': False,
                'filtered_posting': False
            }
        }

class RawJobPostingUpdateRequest(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    source_url: Optional[str] = None
    posting_url: Optional[str] = None
    geolocalization: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    work_schedule: Optional[str] = None
    shift_type: Optional[str] = None
    employment_type: Optional[str] = None
    slots_avaliable: Optional[str] = None
    urgency_required: Optional[bool] = None
    seniority_level: Optional[str] = None
    driving_level: Optional[str] = None
    posting_service: Optional[str] = None
    description: Optional[str] = None
    requisites: Optional[str] = None
    pills: Optional[str] = None
    inclusive_posting: Optional[bool] = None
    published_date: Optional[str] = None
    closing_date: Optional[str] = None
    scanned_date: Optional[str] = None
    normalized_date: Optional[str] = None
    detailed_scan: Optional[bool] = None
    filtered_posting: Optional[bool] = None

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'The title of the Job Posting',
                'source_url': 'https://trabajando.com/busqueda?enfermeria',
                'posting_url': 'https://trabajando.com/trabajo/2421234234',
                'geolocalization': 'Buin, Región Metropolitana',
                'company': 'Hospital de Buín',
                'salary': '12000000',
                'experience': 'No exige',
                'work_schedule': 'Part-Time',
                'shift_type': '4to turno',
                'employment_type': 'A honorarios',
                'slots_available': '2',
                'urgency_required': False,
                'seniority_level': 'Práctica',
                'driving_level': '',
                'posting_service': 'Trabajando',
                'description': 'Se requiere enfermera de práctica',
                'requisites': 'Titulada',
                'pills': 'full-time | 4o turno | 400.000',
                'inclusive_posting': False,
                'published_date': 'hace 2 días',
                'closing_date': '',
                'scanned_date': '2023-11-23 18:54:33:3455322',
                'normalized_date': '',
                'detailed_scan': False,
                'filtered_posting': False
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_posts(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(RawJobsPostings).limit(25).all()

@router.get("/{job_id}", status_code=status.HTTP_200_OK)
async def read_raw_job_posting_data(user: user_dependency, db: db_dependency, job_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    raw_job_posting_model = db.query(RawJobsPostings).filter(RawJobsPostings.id == job_id).first()
    
    if raw_job_posting_model is not None:
        return raw_job_posting_model
    raise HTTPException(status_code=404, detail='Raw Job Posting not found.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_raw_job_posting(user: user_dependency, db: db_dependency,raw_job_posting_request: RawJobPostingRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    raw_job_posting_model = RawJobsPostings(**raw_job_posting_request.model_dump())

    check = db.query(RawJobsPostings).filter(RawJobsPostings.posting_url == raw_job_posting_model.posting_url).first()
    if not check:
        db.add(raw_job_posting_model)
        db.commit()
        db.refresh(raw_job_posting_model)
        return {'new_entry_id': raw_job_posting_model.id}
    else:
        raise HTTPException(status_code=409, detail="Job Posting already exists")

@router.put("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_posting_in_detail(user: user_dependency, db: db_dependency, raw_job_posting_update_request: RawJobPostingUpdateRequest, job_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    raw_job_posting_model = db.query(RawJobsPostings).filter(RawJobsPostings.id == job_id).first()
    if raw_job_posting_model is None:
        raise HTTPException(status_code=404, detail='Job Posting not found.')
    
    if raw_job_posting_update_request.title != None: raw_job_posting_model.title = raw_job_posting_update_request.title
    if raw_job_posting_update_request.source_url != None: raw_job_posting_model.source_url = raw_job_posting_update_request.source_url    
    if raw_job_posting_update_request.posting_url != None: raw_job_posting_model.posting_url = raw_job_posting_update_request.posting_url
    if raw_job_posting_update_request.geolocalization != None: raw_job_posting_model.geolocalization = raw_job_posting_update_request.geolocalization
    if raw_job_posting_update_request.company != None: raw_job_posting_model.company = raw_job_posting_update_request.company     
    if raw_job_posting_update_request.salary != None: raw_job_posting_model.salary = raw_job_posting_update_request.salary
    if raw_job_posting_update_request.experience != None: raw_job_posting_model.experience = raw_job_posting_update_request.experience
    if raw_job_posting_update_request.work_schedule != None: raw_job_posting_model.work_schedule = raw_job_posting_update_request.work_schedule
    if raw_job_posting_update_request.shift_type != None: raw_job_posting_model.shift_type = raw_job_posting_update_request.shift_type
    if raw_job_posting_update_request.employment_type != None: raw_job_posting_model.employment_type = raw_job_posting_update_request.employment_type
    if raw_job_posting_update_request.slots_avaliable != None: raw_job_posting_model.slots_avaliable = raw_job_posting_update_request.slots_avaliable
    if raw_job_posting_update_request.urgency_required != None: raw_job_posting_model.urgency_required = raw_job_posting_update_request.urgency_required
    if raw_job_posting_update_request.seniority_level != None: raw_job_posting_model.seniority_level = raw_job_posting_update_request.seniority_level
    if raw_job_posting_update_request.driving_level != None: raw_job_posting_model.driving_level = raw_job_posting_update_request.driving_level
    if raw_job_posting_update_request.posting_service != None: raw_job_posting_model.posting_service = raw_job_posting_update_request.posting_service
    if raw_job_posting_update_request.description != None: raw_job_posting_model.description = raw_job_posting_update_request.description
    if raw_job_posting_update_request.requisites != None: raw_job_posting_model.requisites = raw_job_posting_update_request.requisites
    if raw_job_posting_update_request.pills != None: raw_job_posting_model.pills = raw_job_posting_update_request.pills
    if raw_job_posting_update_request.inclusive_posting != None: raw_job_posting_model.inclusive_posting = raw_job_posting_update_request.inclusive_posting
    if raw_job_posting_update_request.published_date != None: raw_job_posting_model.published_date = raw_job_posting_update_request.published_date
    if raw_job_posting_update_request.closing_date != None: raw_job_posting_model.closing_date = raw_job_posting_update_request.closing_date
    if raw_job_posting_update_request.scanned_date != None: raw_job_posting_model.scanned_date = raw_job_posting_update_request.scanned_date
    if raw_job_posting_update_request.normalized_date != None: raw_job_posting_model.normalized_date = raw_job_posting_update_request.normalized_date
    if raw_job_posting_update_request.detailed_scan != None: raw_job_posting_model.detailed_scan = raw_job_posting_update_request.detailed_scan
    if raw_job_posting_update_request.filtered_posting != None: raw_job_posting_model.filtered_posting = raw_job_posting_update_request.filtered_posting

    raw_job_posting_model.detailed_scan = True
    db.add(raw_job_posting_model)
    db.commit()

#    @router.get("/filtered/", status_code=status.HTTP_200_OK)
# async def read_job_offers_by_detailed_scan(user: user_dependency, db: db_dependency, posting_service: str):

#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
    
#     postings = db.query(RawJobsPostings).\
#         filter(RawJobsPostings.detailed_scan == False).\
#         filter(RawJobsPostings.filtered_posting == False).\
#         filter(RawJobsPostings.posting_service == posting_service).\
#         slice(0,25).\
#         all()
#     post_dict = []
#     for u in postings:
#         temp_dict = {"id": u.id, "posting_url": u.posting_url}
#         post_dict.append(temp_dict)

#     if post_dict == []:
#         raise HTTPException(status_code=404, detail="No Job posting to Scan in detail")
#     return post_dict