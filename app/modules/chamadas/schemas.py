from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.modules.assistidos.schemas import AssistidoResponse
from app.modules.aulas.schemas import AulaResponse

class ItemChamada(BaseModel):
    assistido_id: int = Field(..., description="ID do aluno/assistido")
    presente: bool = Field(..., description="True para presente, False para ausente")
    observacao: Optional[str] = Field(None, max_length=255, description="Observações")

class ChamadaLoteCreate(BaseModel):
    aula_id: int = Field(..., description="ID da aula")
    presencas: List[ItemChamada] = Field(..., description="Lista de presença dos alunos")

class ChamadaUpdate(BaseModel):
    presente: Optional[bool] = Field(None, description="Status presença")
    observacao: Optional[str] = Field(None, max_length=255, description="Observações")

class ChamadaResponse(BaseModel):
    id: int 
    aula_id: int 
    assistido_id: int 
    presente: bool 
    observacao: Optional[str]
    registrado_em: datetime

    aula: Optional[AulaResponse] = Field(None, description="Dados da Aula")
    assistido: Optional[AssistidoResponse] = Field(None, description="Dados do Aluno")

    model_config = ConfigDict(from_attributes=True)