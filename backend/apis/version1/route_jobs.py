from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import List

from db.session import get_db
from db.base import Job, User
from schemas.jobs import JobCreate, ShowJob
from db.repository.jobs import create_new_job, retrieve_job, list_jobs, update_job_by_id, delete_job_by_id
from apis.version1.route_login import get_current_user_form_token

router = APIRouter()


@router.post('/create-job/', response_model=ShowJob)
def create_job(job: JobCreate,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user_form_token)
               ):
    """
    создаем маршрут, который будет получать данные для создания работы, методом POST
    """
    job = create_new_job(job=job, db=db, owner_id=current_user.id)
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


@router.get('/all', response_model=List[ShowJob])
def read_all_job(db: Session = Depends(get_db)):
    """
    создаем маршрут, для чтение всех вакансий
    """
    jobs = list_jobs(db=db)
    return jobs


@router.put('/update/{id_job}')
def update_job(id_job: int, job: JobCreate, db: Session = Depends(get_db)):
    """
    создаем маршрут, для обновление конкретной вакансии
    """
    current_user = 1
    message = update_job_by_id(id_job=id_job, job=job, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Работа с идентификатором {id_job} не существует"
                            )
    return {'msg': 'Успешное обновление данных'}


@router.delete('/delete/{id_job}')
def delete_job(id_job: int,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user_form_token)
               ):
    """
    создаем маршрут, для удаление конкретной вакансии
    """
    job = retrieve_job(id_job=id_job, db=db)
    if not job:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Работа с идентификатором {id_job} не существует')
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id_job=id_job, db=db, owner_id=current_user.id)
        return {'msg': 'Успешное удаление данных'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Вам не разрешено удалять вакансию № {id_job}, так как вы не размещали ее!!!!"
                        )
