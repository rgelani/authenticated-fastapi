from enum import Enum

class AuthProvider(str, Enum):
    PASSWORD = "password"
    GOOGLE = "google"
    GITHUB = "github"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"    