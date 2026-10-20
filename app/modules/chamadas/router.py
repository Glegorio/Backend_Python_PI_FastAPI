from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.chamadas.schemas import (
    ChamadaLoteCreate,
    ChamadaResponse,
    ChamadaUpdate,
)
from app.modules.chamadas.service import ChamadaService

router = APIRouter(prefix="/chamadas", tags=["Chamadas das Aulas (Presença)"])

@router.post(
    "/lote",
    response_model=List[ChamadaResponse],
    status_code=status.HTTP_200_OK,
    summary="Registrar ou atualizar a chamada de uma aula em lote",
)
async def registrar_chamada_em_lote(
    data: ChamadaLoteCreate, db: AsyncSession = Depends(get_db)
):
    service = ChamadaService(db)
    return await service.registrar_chamada_lote(data)

@router.get(
    "/aula/{aula_id}",
    response_model=List[ChamadaResponse],
    summary="Consultar a lista de chamada/presença de uma aula específica",
)
async def obter_chamada_da_aula(aula_id: int, db: AsyncSession = Depends(get_db)):
    service = ChamadaService(db)
    return await service.get_by_aula(aula_id)

@router.patch(
    "/{chamada_id}",
    response_model=ChamadaResponse,
    summary="Atualizar a presença de um aluno individualmente",
)
async def atualizar_presenca_individual(
    chamada_id: int,
    data: ChamadaUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ChamadaService(db)
    chamada_atualizada = await service.update(chamada_id, data)
    if not chamada_atualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de chamada não encontrado"
        )
    return chamada_atualizada