from sqlmodel import create_engine, SQLModel, Session, select
from app.models import Employee, Department, Dependent
from app.core.configs import Config

if Config.DB.URL.startswith("sqlite"):
    engine = create_engine(Config.DB.URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(Config.DB.URL)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
def department_exists(department_id: int):
    with Session(engine) as session:
        return session.exec(select(Department).where(Department.id == department_id)).first() is not None
if __name__ == "__main__":
    create_tables()