from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    developer = "developer"
    tester = "tester"
    manager = "manager"
    user = "user"


class StatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    READY_FOR_TEST = "READY_FOR_TEST"
    DONE = "DONE"