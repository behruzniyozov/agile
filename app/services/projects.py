from sqlalchemy.orm import Session

from models import Project


def generate_project_key(db: Session, name: str) -> str:
    generated_name = name.upper()[:3]

    how_many_in_db = db.query(Project).filter(Project.name == generated_name).count()

    if how_many_in_db > 0:
        generated_name += str(how_many_in_db + 1)

    return generated_name