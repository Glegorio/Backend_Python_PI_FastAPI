from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Voluntario(Base):
    """Modelo ORM para a tabela de Voluntários no Banco"""

    __tablename__ = "voluntarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome_completo: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    funcao: Mapped[str] = mapped_column(
        String(80),
        nullable=False
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