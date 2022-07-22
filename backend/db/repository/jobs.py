"""
Поскольку мы используем шаблон репозитория и хотим чтобы логика формы базы данных была полностью отделена от
логики маршрутов fastapi, создаем функцию «create_new_job» для логики создания job.
Сдесь хранится БИЗНЕС-ЛОГИКА
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


def retrieve_job(id_job: int, db: Session):
    """
    Получение конкретной вакансии для (end-point '/jobs/get/{id_job}/')
    """
    item = db.query(Job).filter(Job.id == id_job).first()
    return item


def list_jobs(db: Session):
    """
    Получение всех вакансий для (end-point '/jobs/all/')
    """
    jobs = db.query(Job).filter(Job.is_active == True).all()
    return jobs


def update_job_by_id(id_job: int, job: JobCreate, db: Session, owner_id):
    """
    Обновление вакансии для (end-point '/jobs/update/{id_job}')
    """
    existing_job = db.query(Job).filter(Job.id == id_job)
    if not existing_job.first():
        return 0

    print("job.__dict__=======", job.__dict__)
    job.__dict__.update(owner_id=owner_id)  # обновить словарь с новым значением ключа owner_id
    print("job.__dict__=======", job.__dict__)

    existing_job.update(job.__dict__)
    db.commit()
    return 1


def delete_job_by_id(id_job: int, db: Session, owner_id):
    """
    Удаление вакансии для (end-point '/jobs/delete/1')
    """
    existing_job = db.query(Job).filter(Job.id == id_job)
    if not existing_job.first():
        return 0
    # Команда session.query(Child).delete() не только удалит соответствующие объектам Child записи из базы данных,
    # но и обновит состояние этих объектов в сессии.
    # Естественно, эти дополнительные действия требуют времени и соответственно замедлят процесс удаления.
    # Если вы точно знаете, что дальше по коду вы не будете больше обращаться к этим объектам,
    # то вам незачем обновлять их состояние. Для этого и служит synchronize_session=False.
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
