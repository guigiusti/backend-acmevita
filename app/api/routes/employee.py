from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Employee, Dependent
from app.schemas.employee import EmployeePostRequest, EmployeePostResponse, EmployeeGetResponse

router = APIRouter()

@router.get("/employee/{department_id}", response_model=list[EmployeeGetResponse], status_code=status.HTTP_200_OK)
def get_employees_by_department(department_id: int, session: Session = Depends(get_session)) -> list[EmployeeGetResponse]:
    try:
        results = session.exec(select(Employee).where(Employee.department_id == int(department_id))).all()
        if not results:
            return []
        return [
            {
                "name": employee.name,
                "have_dependents": employee.have_dependents 
            }
                for employee in results
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/employee", response_model=EmployeePostResponse, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeePostRequest, session: Session = Depends(get_session)) -> EmployeePostResponse:
    try:
        employee = Employee(
            name=data.name,
            department_id=data.department_id,
            have_dependents=len(data.dependents) > 0,
            dependents=[Dependent(name=dependent.name) for dependent in data.dependents]
        )
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return {
            "id": employee.id,
            "name": employee.name,
            "department_id": employee.department_id,
            "have_dependents": employee.have_dependents,
            "dependents": [{"name": dependent.name} for dependent in employee.dependents]
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))