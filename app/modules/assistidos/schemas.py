from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class AssistidoBase(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=150, description="Nome completo do aluno")
    data_nascimento: date = Field(..., description="Data de nascimento (AAAA-MM-DD)")
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do aluno (opicional)")
    nome_responsavel: str = Field(..., min_length=3, max_length=150, description="Nome do responsável legal")
    telefone_responsavel: str = Field(..., min_length=8, max_length=20, description="Telefone de contato do responsável")
    posicao_campo: Optional[str] = Field("Indefinido", max_length=50, description="Posição em campo (ex: Atacante, Zagueiro)")

class AssistidoCreate(AssistidoBase):
    pass

class AssistidoUpdate(BaseModel):
    nome_completo: Optional[str] = Field(None, min_length=3, max_length=150, description="Nome completo")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento (AAAA-MM-DD)")
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do aluno")
    nome_responsavel: Optional[str] = Field(None, min_length=3, max_length=150, description="Nome do responsável legal")
    telefone_responsavel: Optional[str] = Field(None, min_length=8, max_length=20, description="Telefone de contato")
    posicao_campo: Optional[str] = Field(None, max_length=50, description="Posição em campo")
    ativo: Optional[bool] = Field(None, description="Status de ativo/inativo")

class AssistidoResponse(AssistidoBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime 

    model_config = ConfigDict(from_attributes=True)