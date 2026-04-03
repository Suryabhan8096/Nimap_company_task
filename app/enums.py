from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    AUDITOR = "auditor"
    CLIENT = "client"
