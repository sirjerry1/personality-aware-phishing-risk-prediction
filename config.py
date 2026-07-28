import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-secret-key"
    )

    DATABASE = os.environ.get(
        "DATABASE",
        os.path.abspath("research.db")
    )