from typing import Annotated, Optional, Union
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status
from models import Spiders, Users, Errors, Messages
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/logs',
    tags=['logs']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class SpidersRequest(BaseModel):
    id: Optional[int] = None
    job_id: Optional[str] = None
    spider_name: Optional[str] = None
    scheduled_status: Optional[str] = None
    exit_status: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    memusage_startup: Optional[float] = None
    memusage_max: Optional[float] = None
    elapsed_time_seconds: Optional[float] = None
    items_scraped: Optional[int] = None
    items_saved: Optional[int] = None
    posting_service: Optional[str] = None

    class Config:
        json_schema_extra = {
            'example': {
                'job_id': 'c6c78fe693d111ee8d5d0242ac1e0004',
                'spider_name': 'cltrablisting',
                'scheduled_status': 'ok',
                'exit_status': 'finished',
                'start_time': '2023, 12, 6, 0, 52, 53, 361408, tzinfo=datetime.timezone.utc',
                'end_time': '2023, 12, 6, 0, 53, 5, 717977, tzinfo=datetime.timezone.utc',
                'memusage_startup': '66183168',
                'memusage_max': '66183168',
                'elapsed_time_seconds': '12.356569',
                'items_scraped': '30',
                'items_saved': '2',
                'posting_service': 'Chiletrabajo',
            }
        }

class ErrorsRequest(BaseModel):
    id: Optional[int] = None
    docker_name: Optional[str] = None
    process_name: Optional[str] = None
    service_ip: Optional[str] = None
    error_type: Optional[str] = None
    pushed_status: Optional[str] = None
    creation_time: Optional[str] = None
    spider_name: Optional[str] = None
    posting_service: Optional[str] = None
    error_detail: Optional[str] = None
    http_status_code: Optional[int] = None
    website_error: Optional[str] = None

    class Config:
        json_schema_extra = {
            'example': {
                'docker_name': 'scrapper',
                'process_name': 'scrapy',
                'service_ip': '172.195.1.24',
                'error_type': 'DOMError',
                'pushed_status': 'False',
                'creation_time': '2023, 12, 6, 0, 52, 53, 361408, tzinfo=datetime.timezone.utc',
                'spider_name': 'cltrablisting',
                'posting_service': 'Chiletrabajo',
                'error_detail': 'Lorem ipsum dolor sit amet',
                'http_status_code': 'None',
                'website_error': 'https://trabajando.com/trabajos/1234232'
            }
        }

@router.get("/spiders", status_code=status.HTTP_200_OK)
async def get_multiple_spider_logs(user: user_dependency, db: db_dependency, 
                                        scheduled_status: str, 
                                        job_id: str, 
                                        exit_status: str):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    logs = db.query(Spiders).\
            filter(Spiders.scheduled_status == scheduled_status).\
            filter(Spiders.job_id == job_id).\
            filter(Spiders.exit_status == exit_status).\
            slice(0,25).\
            all()
    
    if logs:
        return logs
    else:
        raise HTTPException(status_code=404, detail="No Logs found under present filter")

@router.get("/spiders/{spider_log_id}", status_code=status.HTTP_200_OK)
async def get_info_on_logged_spider_run(user: user_dependency, db: db_dependency,
                                        spider_log_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    log = db.query(Spiders).\
            filter(Spiders.id == spider_log_id).\
            first()

    if log:
        return log
    else:
        raise HTTPException(status_code=404, detail="No Log found")


@router.post("/spiders", status_code=status.HTTP_201_CREATED)
async def create_new_scrapper_job(user: user_dependency, db: db_dependency, spider_log_request: SpidersRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    spider_log_model = Spiders(**spider_log_request.model_dump())

    db.add(spider_log_model)
    db.commit()
    db.refresh(spider_log_model)
    
    return {'new_entry_id': spider_log_model.id}



@router.put("/spiders/{spider_log_id}", status_code=status.HTTP_200_OK)
async def update_scrapper_job(user: user_dependency, db: db_dependency, spider_log_request: SpidersRequest, spider_log_id: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    spider_log_model = db.query(Spiders).filter(Spiders.job_id == spider_log_id).first()
    if spider_log_model is None:
        raise HTTPException(status_code=404, detail='Log Spider ID not found.')
    
    if spider_log_request.spider_name != None: spider_log_model.spider_name = spider_log_request.spider_name
    if spider_log_request.scheduled_status != None: spider_log_model.scheduled_status = spider_log_request.scheduled_status
    if spider_log_request.exit_status != None: spider_log_model.exit_status = spider_log_request.exit_status
    if spider_log_request.start_time != None: spider_log_model.start_time = spider_log_request.start_time
    if spider_log_request.end_time != None: spider_log_model.end_time = spider_log_request.end_time
    if spider_log_request.memusage_startup != None: spider_log_model.memusage_startup = spider_log_request.memusage_startup
    if spider_log_request.memusage_max != None: spider_log_model.memusage_max = spider_log_request.memusage_max
    if spider_log_request.elapsed_time_seconds != None: spider_log_model.elapsed_time_seconds = spider_log_request.elapsed_time_seconds
    if spider_log_request.items_scraped != None: spider_log_model.items_scraped = spider_log_request.items_scraped
    if spider_log_request.items_saved != None: spider_log_model.items_saved = spider_log_request.items_saved

    db.add(spider_log_model)
    db.commit()


@router.post("/errors", status_code=status.HTTP_201_CREATED)
async def create_error_log(db: db_dependency, error_log_request: ErrorsRequest):
    
    error_log_model = Errors(**error_log_request.model_dump())

    db.add(error_log_model)
    db.commit()