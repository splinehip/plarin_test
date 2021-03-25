from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    _id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    company: Optional[str] = None
    join_date: Optional[datetime] = None
    job_title: Optional[str] = None
    gender: Optional[str] = None
    salary: Optional[int] = None
