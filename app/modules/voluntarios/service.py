from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.voluntarios.models import Voluntario
from app.modules.voluntarios.schemas import VoluntarioCreate, VoluntarioUpdate


class VoluntarioService:
    """Camada de serviço responsável pelas operações de banco e regras de negócio de Voluntários"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100, apenas_ativos: bool = True) -> Sequence[Voluntario]:
        """Retorna uma lista paginada de voluntários"""
        query = select(Voluntario)
        if apenas_ativos:
            query = query.where(Voluntario.ativo == True)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, voluntario_id: int) -> Optional[Voluntario]:
        """Busca um voluntário pelo ID"""
        query = select(Voluntario).where(Voluntario.id == voluntario_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Voluntario]:
        """Busca um voluntário pelo e-mail para evitar registros duplicados"""
        query = select(Voluntario).where(Voluntario.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, schema: VoluntarioCreate) -> Voluntario:
        """Cadastra um novo voluntário no MySQL"""
        novo_voluntario = Voluntario(**schema.model_dump())
        self.db.add(novo_voluntario)
        await self.db.commit()
        await self.db.refresh(novo_voluntario)
        return novo_voluntario

    async def update(self, voluntario_id: int, schema: VoluntarioUpdate) -> Optional[Voluntario]:
        """Atualiza os dados de um voluntário existente"""
        voluntario = await self.get_by_id(voluntario_id)
        if not voluntario:
            return None

        # Atualiza apenas os campos que foram realmente enviados (exclude_unset=True)
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(voluntario, key, value)

        await self.db.commit()
        await self.db.refresh(voluntario)
        return voluntario

    async def delete_soft(self, voluntario_id: int) -> Optional[Voluntario]:
        """Realiza a exclusão lógica (soft delete) desativando o voluntário"""
        voluntario = await self.get_by_id(voluntario_id)
        if not voluntario:
            return None

        voluntario.ativo = False
        await self.db.commit()
        await self.db.refresh(voluntario)
        return voluntario