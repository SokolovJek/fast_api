from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class JobBase(BaseModel):
    """
    Указываем общие свойства модели
    """
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = 'Remote'
    descriptions: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()


class JobCreate(JobBase):
    """
    будет использоваться для проверки данных при создании job
    """
    title: str
    company: str
    location: str
    descriptions: str


class ShowJob(JobBase):
    """
    будет использоваться для форматирования ответа, чтобы в нем не было id, owner_id и т.д.
    """
    title: str
    company: str
    company_url: Optional[str]
    location: str
    descriptions: Optional[str]
    date_posted: date

    class Config:
        """
        преобразование недиктового obj в json
        """
        orm_mode = True
