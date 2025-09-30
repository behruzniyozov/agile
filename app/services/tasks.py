from sqlalchemy.orm import Session

from models import Project


def generate_task_key(db: Session, project: Project) -> str:
    tasks_count = project.tasks.count()

    generated_name = project.key + "-" + str(tasks_count + 1)

    return generated_name