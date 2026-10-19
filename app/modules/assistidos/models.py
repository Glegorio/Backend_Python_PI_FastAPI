from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Date, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Assistido(Base):
    """Modelo ORM para a tabela de Assistidos (Alunos) no MySQL"""

    __tablename__ = "assistidos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome_completo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )

    data_nascimento: Mapped[date] = mapped_column(
        Date,
        nullable=False, 
    )

    cpf: Mapped[Optional[str]] = mapped_column(
        String(14),
        unique=True,
        nullable=True
    )

    nome_responsavel: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    telefone_responsavel: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    posicao_campo: Mapped[Optional[str]] = mapped_column(
        String(50),
        default="Indefinido"
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(), 
        nullable=False
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )