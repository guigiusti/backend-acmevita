from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime, timezone
if TYPE_CHECKING:
    from app.models.dependent import Dependent
    from app.models.department import Department

class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    department_id: int = Field(foreign_key="departments.id")
    have_dependents: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None)
    dependents: list["Dependent"] = Relationship(back_populates="employee")
    department: "Department" = Relationship(back_populates="employees")