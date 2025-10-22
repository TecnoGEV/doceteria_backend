from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import (
    ReceitaModel,
)
from src.scherma import (
    ReceitaScherma,
)

receita_router = APIRouter()
tag = "Receita"

@receita_router.get(
    "/receitas",
    tags=[tag],
    name="receita_index",
    summary="Receita Index",
    description="Receita Index",
    response_description="Receita Index",
    status_code=200,
    response_model=list[ReceitaScherma],
)
def listar_receitas(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> List[ReceitaModel]:
    """
    Retorna uma lista paginada de receitas.
    """
    offset = (page - 1) * page_size
    receitas = db.query(ReceitaModel).offset(offset).limit(page_size).all()
    return receitas


@receita_router.post(
    "/receitas",
    tags=[tag],
    name="receita_create",
    summary="Receita Create",
    description="Receita Create",
    response_description="Receita Create",
    status_code=201,
    response_model=ReceitaScherma,
)
async def create_receita(
    receita: ReceitaScherma, db: Annotated[Session, Depends(get_db)]
) -> ReceitaModel:
    """
    Cria uma nova receita.

    Parameters:
    receita (Receita): Receita a ser criada.

    Returns:
    Receita: A nova receita criada.
    """
    db_receita = ReceitaModel(**receita.model_dump())
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita


@receita_router.get(
    "/receita/{id}",
    tags=[tag],
    name="receita_show",
    summary="Receita Show",
    description="Receita Show",
    response_description="Receita Show",
    status_code=200,
    response_model=ReceitaScherma,
)
async def show_receita(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> ReceitaModel | None:
    """
    Mostra uma receita existente.

    Parameters:
    id (int): O ID da receita a ser mostrada.

    Returns:
    Receita: A receita existente com o ID informado.
    """
    return db.query(ReceitaModel).filter(ReceitaModel.id == id_).first()


@receita_router.patch(
    "/receita/{id}",
    tags=[tag],
    name="receita_update",
    summary="Receita Update",
    description="Receita Update",
    response_description="Receita Update",
    status_code=200,
    response_model=ReceitaScherma,
)
async def update_receita(
    id_: int, receita: ReceitaScherma, db: Annotated[Session, Depends(get_db)]
) -> ReceitaModel | None:
    """
    Atualiza uma receita existente.

    Parameters:
    id (int): O ID da receita a ser atualizada.
    receita (Receita): A receita com as informações atualizadas.

    Returns:
    Receita: A receita atualizada.
    """
    data = receita.model_dump(exclude_unset=True)
    stmt = (
        update(ReceitaModel)
        .where(ReceitaModel.id == id_)
        .values({getattr(ReceitaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(ReceitaModel).filter(ReceitaModel.id == id_).first()


@receita_router.delete(
    "/receita/{id}",
    tags=[tag],
    name="receita_delete",
    summary="Receita Delete",
    description="Receita Delete",
    response_description="Receita Delete",
    status_code=204,
)
async def delete_receita(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    """
    Remove uma receita pelo seu ID.

    Parameters:
    id (int): O ID da receita a ser removida.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(ReceitaModel).filter(ReceitaModel.id == id_).delete()
    db.commit()
    return JSONResponse("Receita removida com sucesso.", status_code=204)
