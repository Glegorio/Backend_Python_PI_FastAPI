from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.modules.aulas.models import Aula
from app.modules.aulas.schemas import AulaCreate, AulaUpdate
from app.modules.voluntarios.service import VoluntarioService

class AulaService:
    """Camada de serviço responsável pelas operações de banco e regras de negócio de Aulas"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Aula]:
        """Retorna uma lista paginada de aulas trazendo os dados do voluntário responsável"""
        query = (
            select(Aula)
            .options(joinedload(Aula.voluntario))
            .offset(skip)
            .limit(limit)
            .order_by(Aula.data_hora.desc())
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, aula_id: int) -> Optional[Aula]:
        """Busca uma aula pelo ID trazendo o voluntário relacionado"""
        query =(
            select(Aula)
            .options(joinedload(Aula.voluntario))
            .where(Aula.id == aula_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, schema: AulaCreate) -> Optional[Aula]:
        """Cadastra uma nova aula no Banco validando a existência do voluntário"""
        voluntario_service = VoluntarioService(self.db)
        voluntario = await voluntario_service.get_by_id(schema.voluntario_id)
        if not voluntario or not voluntario.ativo:
            return None 

        nova_aula = Aula(**schema.model_dump())
        self.db.add(nova_aula)
        await self.db.commit()
        await self.db.refresh(nova_aula)

        # Recarrega a aula com os dados do voluntário para a resposta 
        return await self.get_by_id(nova_aula.id)

    async def update(self, aula_id: int, schema: AulaUpdate) -> Optional[Aula]:
        """Atualiza os dados de uma aula existente"""
        aula = await self.get_by_id(aula_id)
        if not aula:
            return None 

        # Se alterar o voluntário, valida se o novo voluntário existe
        if schema.voluntario_id is not None:
            voluntario_service = VoluntarioService(self.db)
            voluntario = await voluntario_service.get_by_id(schema.voluntario_id)
            if not voluntario or not voluntario.ativo:
                return None 

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(aula, key, value)

        await self.db.commit()
        await self.db.refresh(aula)
        return await self.get_by_id(aula_id)

    async def delete(self, aula_id: int) -> bool:
        """Remove uma aula cadastrada"""
        aula = await self.get_by_id(aula_id)
        if not aula:
            return False

        await self.db.delete(aula)
        await self.db.commit()
        return True 