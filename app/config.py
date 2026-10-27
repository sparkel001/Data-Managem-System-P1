import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Settings:
    mongo_uri: str = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")
    database: str = os.getenv("MONGODB_DATABASE", "survey_system")
