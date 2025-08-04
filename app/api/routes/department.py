from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Department
from app.schemas.department import DepartmentGetResponse, DepartmentPostRequest, DepartmentPostResponse

router = APIRouter()

@router.get("/department", response_model=list[DepartmentGetResponse], status_code=status.HTTP_200_OK)
def get_departments(session: Session = Depends(get_session)) -> list[DepartmentGetResponse]:
    try:
        results = session.exec(select(Department)).all()
        if not results:
            return []
        return [{
            "id": department.id,  
            "name": department.name,
        } for department in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/department", response_model=DepartmentPostResponse, status_code=status.HTTP_201_CREATED)
def create_department(data: DepartmentPostRequest, session: Session = Depends(get_session)) -> DepartmentPostResponse:
    try:
        department = Department(name=data.name)
        session.add(department)
        session.commit()
        session.refresh(department)
        return {
            "id": department.id,
            "name": department.name,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))