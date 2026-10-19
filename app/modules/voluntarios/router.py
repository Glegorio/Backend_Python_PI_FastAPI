from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.voluntarios.schemas import (
    VoluntarioCreate,
    VoluntarioResponse,
    VoluntarioUpdate,
)
from app.modules.voluntarios.service import VoluntarioService

router = APIRouter(prefix="/voluntarios", tags=["Voluntários (Equipe/Treinadores)"])


@router.post(
    "/",
    response_model=VoluntarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo voluntário",
)
async def criar_voluntario(
    data: VoluntarioCreate, db: AsyncSession = Depends(get_db)
):
    service = VoluntarioService(db)

    # Validação de duplicidade de e-mail
    existente = await service.get_by_email(data.email)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um voluntário cadastrado com este e-mail.",
        )

    return await service.create(data)


@router.get(
    "/",
    response_model=List[VoluntarioResponse],
    summary="Listar voluntários cadastrados",
)
async def listar_voluntarios(
    skip: int = 0,
    limit: int = 100,
    apenas_ativos: bool = True,
    db: AsyncSession = Depends(get_db),
):
    service = VoluntarioService(db)
    return await service.get_all(
        skip=skip, limit=limit, apenas_ativos=apenas_ativos
    )


@router.get(
    "/{voluntario_id}",
    response_model=VoluntarioResponse,
    summary="Buscar voluntário por ID",
)
async def obter_voluntario(voluntario_id: int, db: AsyncSession = Depends(get_db)):
    service = VoluntarioService(db)
    voluntario = await service.get_by_id(voluntario_id)
    if not voluntario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voluntário não encontrado.",
        )
    return voluntario


@router.patch(
    "/{voluntario_id}",
    response_model=VoluntarioResponse,
    summary="Atualizar dados de um voluntário",
)
async def atualizar_voluntario(
    voluntario_id: int,
    data: VoluntarioUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = VoluntarioService(db)
    voluntario_atualizado = await service.update(voluntario_id, data)
    if not voluntario_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voluntário não encontrado.",
        )
    return voluntario_atualizado


@router.delete(
    "/{voluntario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativar um voluntário (Soft Delete)",
)
async def desativar_voluntario(
    voluntario_id: int, db: AsyncSession = Depends(get_db)
):
    service = VoluntarioService(db)
    voluntario = await service.delete_soft(voluntario_id)
    if not voluntario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voluntário não encontrado.",
        )
    return None