from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Boolean, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.aulas.models import Aula
    from app.modules.assistidos.models import Assistido

class Chamada(Base):
    """Modelo ORM para a tabela de Chamadas/Presenças do Banco"""

    __tablename__ = "chamadas"
    __table_args__ = (
        # Impede que o mesmo aluno tenha mais de um registro na mesma aula
        UniqueConstraint("aula_id", "assistido_id", name="uk_aula_assistido"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    aula_id: Mapped[int] = mapped_column(
        ForeignKey("aulas.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )

    assistido_id: Mapped[int] = mapped_column(
        ForeignKey("assistidos.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )

    presente: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    observacao: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    registrado_em: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    aula: Mapped["Aula"] = relationship("Aula", lazy="joined")
    assistido: Mapped["Assistido"] = relationship("Assistido", lazy="joined")