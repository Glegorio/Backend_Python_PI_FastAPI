from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.aulas.schemas import (
    AulaCreate,
    AulaResponse,
    AulaUpdate,
)
from app.modules.aulas.service import AulaService

router = APIRouter(prefix="/aulas", tags=["Aulas / Treinos"])

@router.post(
    "/",
    response_model=AulaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar/Agendar uma nova aula",
)
async def criar_aula(data: AulaCreate, db: AsyncSession = Depends(get_db)):
    service = AulaService(db)
    nova_aula = await service.create(data)
    if not nova_aula:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível agenda a aula. Verifique se o voluntário responsável existe e está ativo"
        )
    return nova_aula

@router.get(
    "/",
    response_model=List[AulaResponse],
    summary="Listar aulas agendadas",
)
async def listar_aulas(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    service = AulaService(db)
    return await service.get_all(skip=skip, limit=limit)

@router.get(
    "/{aula_id}",
    response_model=AulaResponse,
    summary="Buscar detalhes de uma aula por ID",
)
async def obter_aula(aula_id: int, db: AsyncSession = Depends(get_db)):
    service = AulaService(db)
    aula = await service.get_by_id(aula_id)
    if not aula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )
    return aula

@router.patch(
    "/{aula_id}",
    response_model=AulaResponse,
    summary="Atualizar dados de uma aula",
)
async def atualizar_aula(
    aula_id: int,
    data: AulaUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = AulaService(db)
    aula_atualizada = await service.update(aula_id, data)
    if not aula_atualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada ou ID do voluntário informado é inválido"
        )
    return aula_atualizada

@router.delete(
    "/{aula_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma aula agendada",
)
async def excluir_aula(aula_id: int, db: AsyncSession = Depends(get_db)):
    service = AulaService(db)
    sucesso = await service.delete(aula_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aula não encontrada"
        )
    return None