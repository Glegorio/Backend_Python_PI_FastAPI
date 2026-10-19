from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.assistidos.models import Assistido
from app.modules.assistidos.schemas import AssistidoCreate, AssistidoUpdate

class AssistidoService:
    """Camada de serviço responsável pelas operações de banco  e regras de negócio"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100, apenas_ativos: bool = True) -> Sequence[Assistido]:
        """Retorna uma lista paginada de assistidos"""
        query = select(Assistido)
        if apenas_ativos:
            query = query.where(Assistido.ativo == True)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, assistido_id: int) -> Optional[Assistido]:
        """Busca um assistido pelo ID"""
        query = select(Assistido).where(Assistido.id == assistido_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_cpf(self, cpf: str) -> Optional[Assistido]:
        """Busca um assistido pelo CPF para evitar duplicidades"""
        query = select(Assistido).where(Assistido.cpf == cpf)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, schema: AssistidoCreate) -> Assistido:
        """Cadastra um novo assistido no Banco de Dados"""
        novo_assistido = Assistido(**schema.model_dump())
        self.db.add(novo_assistido)
        await self.db.commit()
        await self.db.refresh(novo_assistido)
        return novo_assistido

    async def update(self, assistido_id: int, schema: AssistidoUpdate) -> Optional[Assistido]:
        """Atualiza os dados de um assistido existente"""
        assistido = await self.get_by_id(assistido_id)
        if not assistido:
            return None

        # Atualiza apenas os campos enviados no JSON
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(assistido, key, value)

        await self.db.commit()
        await self.db.refresh(assistido)
        return assistido

    async def delete_soft(self, assistido_id: int) -> Optional[Assistido]:
        """Realiza a exclusão lógica (soft delete) desativando o assistido"""
        assistido = await self.get_by_id(assistido_id)
        if not assistido:
            return None

        assistido.ativo = False
        await self.db.commit()
        await self.db.refresh(assistido)
        return assistido 