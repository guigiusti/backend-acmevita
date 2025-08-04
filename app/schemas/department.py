from typing import List
from pydantic import BaseModel, Field, field_validator
from markupsafe import escape

class DepartmentGetResponse(BaseModel):
    id: int
    name: str

class DepartmentPostRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    @field_validator("name")
    def sanitize_name(cls, v: str) -> str:
        return escape(str(v))

class DepartmentPostResponse(BaseModel):
    id: int
    name: str