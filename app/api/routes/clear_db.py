from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, delete, text
from app.core.db import get_session
from app.models.employee import Employee
from app.models.dependent import Dependent
from app.models.department import Department
from app.core.configs import Config
router = APIRouter()

@router.delete("/clear-db", status_code=status.HTTP_204_NO_CONTENT)
def clear_db(session: Session = Depends(get_session)) -> None:
    try:
        if Config.DB.URL.startswith("sqlite"):
            session.exec(delete(Dependent))
            session.exec(delete(Employee))
            session.exec(delete(Department))
        else:
            session.exec(
                text(
                    """
                    TRUNCATE TABLE dependents, employees, departments
                    RESTART IDENTITY CASCADE;
                    """
                )
            )
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))