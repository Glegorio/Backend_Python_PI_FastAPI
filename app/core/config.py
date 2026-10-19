from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Ajustado para .parent.parent (agora aponta corretamente para a raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR.parent / ".env" if (BASE_DIR.parent / ".env").exists() else BASE_DIR / ".env"


class Settings(BaseSettings):
    """Configurações globais da aplicação carregadas do arquivo .env"""

    PROJECT_NAME: str = "ONG Valentes de Davi Backend API"
    VERSION: str = "V.0.0.1"
    API_V1_STR: str = "/api/v1"

    # Permite um valor padrão temporário para a checagem do Pylance não reclamar
    DATABASE_URL: str = "mysql+aiomysql://root:root@localhost:3306/ong_futebol"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instância única das configurações para ser importada na aplicação
settings = Settings()