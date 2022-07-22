from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from db.session import get_db
from db.models.jobs import Job
from schemas.jobs import JobCreate, ShowJob
from db.repository.jobs import create_new_job, retrieve_job

router = APIRouter()


@router.post('/create-job/', response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    создаем маршрут, который будет получать данные для создания работы, методом POST
    """
    current_user = 1
    job = create_new_job(job=job, db=db, owner_id=current_user)
    return job


@router.get('/get/{id_job}', response_model=ShowJob)
def read_job(id_job: int, db: Session = Depends(get_db)):
    """
    создаем маршрут, для чтение конкретной вакансии
    """
    job = retrieve_job(id_job=id_job, db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Работа с идентификатором {id_job} не существует"
                            )
    return job
