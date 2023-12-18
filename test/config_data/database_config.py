import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    name: str


def load_database_config() -> DatabaseConfig:
    load_dotenv()
    return DatabaseConfig(name=os.getenv("DB_NAME"))
