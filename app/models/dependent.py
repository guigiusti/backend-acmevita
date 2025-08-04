from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.employee import Employee

class Dependent(SQLModel, table=True):
    __tablename__ = "dependents"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    employee_id: int = Field(foreign_key="employees.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)
    employee: "Employee" = Relationship(back_populates="dependents")
