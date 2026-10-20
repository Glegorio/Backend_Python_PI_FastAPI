from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.modules.voluntarios.schemas import VoluntarioResponse

class AulaBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, description="Título da aula (ex: Treino Sub-13 Tático)")
    descricao: Optional[str] = Field(None, description="Descrição do plano de treino")
    data_hora: datetime = Field(..., description="Data e hora da aula (AAAA-MM-DD HH:MM:SS)")
    local: str = Field(..., min_length=2, max_length=150, description="Local da aula (ex: Campo 1, Quadra Coberta)")
    voluntario_id: int = Field(..., description="ID do voluntário/treinador responsável")


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=100, description="Título da aula")
    descricao: Optional[str] = Field(None, description="Descrição do plano de treino")
    data_hora: Optional[datetime] = Field(None, description="Data e hora da aula")
    local: Optional[str] = Field(None, min_length=2, max_length=150, description="Local da aula")
    voluntario_id: Optional[int] = Field(None, description="ID do voluntário/treinador responsável")


class AulaResponse(AulaBase):
    id: int
    voluntario: Optional[VoluntarioResponse] = Field(None, description="Dados completos do voluntário responsável")
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)