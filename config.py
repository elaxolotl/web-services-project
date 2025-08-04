import secrets
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    API_TITLE = "Gavel"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = secrets.token_hex(32)
    SECURITY_REGISTERABLE = True
    PROPAGATE_EXCEPTIONS = True
    SECURITY_SEND_REGISTER_EMAIL = False
    OPENAPI_SECURITY_SCHEMES = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    OPENAPI_SECURITY = [{"BearerAuth": []}]
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
