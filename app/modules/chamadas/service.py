from typing import Sequence, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.modules.chamadas.models import Chamada
from app.modules.chamadas.schemas import ChamadaLoteCreate, ChamadaUpdate

class ChamadaService:
    """Camada de serviço responsável pelo registro de chamadas e histórico de presenças"""

    def __init__(self, db: AsyncSession):
        self.db = db 

    async def get_by_aula(self, aula_id: int) -> Sequence[Chamada]:
        """Retorna todas as presenças/faltas registradas para uma aula específica"""
        query = (
            select(Chamada)
            .options(joinedload(Chamada.assistido), joinedload(Chamada.aula))
            .where(Chamada.aula_id == aula_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, chamada_id: int) -> Optional[Chamada]:
        """Busca um registo individual de chamada pelo ID"""
        query =(
            select(Chamada)
            .options(joinedload(Chamada.assistido), joinedload(Chamada.aula))
            .where(Chamada.id == chamada_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def registrar_chamada_lote(self, schema: ChamadaLoteCreate) -> List[Chamada]:
        """
        Registra ou atualiza a chamada de vários alunos para uma determinada aula
        """
        registros_salvos: List[Chamada] = []

        for item in schema.presencas:
            query = select(Chamada).where(
                Chamada.aula_id == schema.aula_id,
                Chamada.assistido_id == item.assistido_id
            )
            result = await self.db.execute(query)
            chamada_existente = result.scalar_one_or_none()

            if chamada_existente:
                chamada_existente.presente = item.presente
                chamada_existente.observacao = item.observacao
                registros_salvos.append(chamada_existente)
            else:
                nova_chamada = Chamada(
                    aula_id=schema.aula_id,
                    assistido_id=item.assistido_id,
                    presente=item.presente,
                    observacao=item.observacao
                )
                self.db.add(nova_chamada)
                registros_salvos.append(nova_chamada)

        await self.db.commit()

        return list(await self.get_by_aula(schema.aula_id))

    async def update(self, chamada_id: int, schema: ChamadaUpdate) -> Optional[Chamada]:
        """Atualiza o status de presença de um aluno individualmente"""
        chamada = await self.get_by_id(chamada_id)
        if not chamada:
            return None 

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(chamada, key, value)

        await self.db.commit()
        await self.db.refresh(chamada)
        return await self.get_by_id(chamada_id)