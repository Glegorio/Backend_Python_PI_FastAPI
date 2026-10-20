from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.voluntarios.models import Voluntario

class Aula(Base):
    """Modelo ORM para a tabela de Aulas no Banco"""

    __tablename__ = "aulas"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    descricao: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        index=True
    )

    local: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
    )

    # Chave Estrangeira ligando aula ao voluntário
    voluntario_id: Mapped[int] = mapped_column(
        ForeignKey("voluntarios.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
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

    # Relacionamento com o ORM de Voluntários
    voluntario: Mapped["Voluntario"] = relationship("Voluntario", lazy="joined")