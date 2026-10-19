from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.assistidos.schemas import (
    AssistidoCreate,
    AssistidoResponse,
    AssistidoUpdate,
)
from app.modules.assistidos.service import AssistidoService

router = APIRouter(prefix="/assistido", tags=["Assistidos (Alunos)"])

@router.post(
    "/",
    response_model=AssistidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo assistido",
)
async def criar_assistido(
    data: AssistidoCreate, db: AsyncSession = Depends(get_db)
):
    service = AssistidoService(db)

    # Validação de duplicidade por CPF se o CPF for informado 
    if data.cpf:
        existente = await service.get_by_cpf(data.cpf)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um assistido cadastrado com este CPF.",
            )

    return await service.create(data)

@router.get(
    "/",
    response_model=List[AssistidoResponse],
    summary="Listar assistidos cadastrados",
)
async def listar_assistidos(
    skip: int = 0,
    limit: int = 100,
    apenas_ativos: bool = True,
    db: AsyncSession = Depends(get_db),
):
    service = AssistidoService(db)
    return await service.get_all(
        skip=skip, limit=limit, apenas_ativos=apenas_ativos
    )

@router.get(
    "/{assitido_id}",
    response_model=AssistidoResponse,
    summary="Buscar assistido por ID",
)
async def obter_assistido(assistido_id: int, db: AsyncSession = Depends(get_db)):
    service = AssistidoService(db)
    assistido = await service.get_by_id(assistido_id)
    if not assistido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistido não encontrado"
        )
    return assistido

@router.patch(
    "/{assitido_id}",
    response_model=AssistidoResponse,
    summary="Atualizar dados de um assistido",
)
async def atualizar_assistido(
    assistido_id: int,
    data: AssistidoUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = AssistidoService(db)
    assistido_atualizado = await service.update(assistido_id, data)
    if not assistido_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistido não encontrado"
        )
    return assistido_atualizado

@router.delete(
    "/{assitido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativar um assistido (Soft Delete)",
)
async def desativar_assistido(
    assistido_id: int, db: AsyncSession = Depends(get_db)
):
    service = AssistidoService(db)
    assistido = await service.delete_soft(assistido_id)
    if not assistido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistido não encontrado",
        )
    return None