import os

class Config:
    SECRET_KEY = "555de27cd2aa0f1c5c3f8322c89172667d7cadef487391f986ef90da7287599c"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://anand:yourpassword@localhost/portfolio_ai"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True




