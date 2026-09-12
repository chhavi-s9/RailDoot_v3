from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "RailDoot"
    app_version: str = "2.0.0"
    environment: str = "development"
    database_url: str = f"sqlite:///{BASE_DIR / 'data' / 'abp_integrated.db'}"
    optimizer_time_limit: int = 30
    max_candidates_per_task: int = 12
    frontend_url: str = "http://localhost:3000"
    model_dir: str = str(BASE_DIR / "ml_models")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
