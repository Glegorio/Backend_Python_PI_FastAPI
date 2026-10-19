from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class VoluntarioBase(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=150, description="Nome completo do voluntário")
    email: EmailStr = Field(..., description="E-mail de contato e login")
    telefone: str = Field(..., min_length=8, max_length=20, description="Telefone / WhatsApp")
    funcao: str = Field(..., min_length=2, max_length=80, description="Cargo/Função (ex: Treinador Sub-15, Monitor)")

class VoluntarioCreate(VoluntarioBase):
    pass 

class VoluntarioUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=150, description="Nome completo")
    email: Optional[EmailStr] = Field(None, description="E-mail de contato")
    telefone: Optional[str] = Field(None, min_length=8, max_length=20, description="Telefone")
    funcao: Optional[str] = Field(None, min_length=2, max_length=80, description="Cargo/Função")
    ativo: Optional[bool] = Field(None, description="Status de ativo/inativo")

class VoluntarioResponse(VoluntarioBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)