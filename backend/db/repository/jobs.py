"""
Поскольку мы используем шаблон репозитория и хотим чтобы логика формы базы данных была полностью отделена от
логики маршрутов fastapi, создаем функцию «create_new_job» для логики создания job.
"""

from sqlalchemy.orm import Session

from schemas.jobs import JobCreate
from db.models.jobs import Job


def create_new_job(job: JobCreate, db: Session, owner_id: int):
    """
    Извлекли логику работы с БД из функции create_user(end-point '/user/'),
    для того чтоб в случае чего можно было изменить ORM
    """
    job_object = Job(**job.dict(),
                     owner_id=owner_id
                     )
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def retrieve_job(id_job, db):
    """
    Получение конкретной вакансии для (end-point '/jobs/get/{id_job}/')
    """
    item = db.query(Job).filter(Job.id == id_job).first()
    return item
