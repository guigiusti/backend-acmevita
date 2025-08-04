from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
if TYPE_CHECKING:
    from app.models.employee import Employee

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)
    employees: list["Employee"] = Relationship(back_populates="department")