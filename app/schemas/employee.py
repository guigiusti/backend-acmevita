from typing import List
from pydantic import BaseModel, Field, field_validator
from markupsafe import escape
from app.core.db import department_exists
class Dependent(BaseModel):
    name: str

class EmployeeGetResponse(BaseModel):
    name: str
    have_dependents: bool


class EmployeePostRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    department_id: int = Field(gt=0)
    dependents: List[Dependent] = []
    @field_validator("name")
    def sanitize_name(cls, v: str) -> str:
        return escape(str(v))
    @field_validator("department_id")
    def sanitize_department_id(cls, v: str) -> int:
        if not str(v).isdigit():
            raise ValueError("Department ID must be a number")
        if not department_exists(int(v)):
            raise ValueError("Invalid Department ID")
        return int(v)

class EmployeePostResponse(BaseModel):
    id: int
    name: str
    department_id: int
    have_dependents: bool
    dependents: List[Dependent]