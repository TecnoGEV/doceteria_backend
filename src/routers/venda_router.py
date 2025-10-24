from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models.venda_model import VendaModel
from src.schermas.venda_scherma import VendaScherma

venda_router = APIRouter()
tag = "Venda"


@venda_router.get(
    "/vendas",
    tags=[tag],
    name="venda_index",
    summary="Venda Index",
    description="Venda Index",
    response_description="Venda Index",
    status_code=200,
    response_model=list[VendaScherma],
)
async def venda_index(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> list[VendaModel]:
    """Lista todas as vendas cadastradas."""
    offset = (page - 1) * page_size
    return db.query(VendaModel).offset(offset).limit(page_size).all()


@venda_router.get(
    "/venda/{id}",
    tags=[tag],
    name="venda_show",
    summary="Venda Show",
    description="Venda Show",
    response_description="Venda Show",
    status_code=200,
    response_model=VendaScherma,
)
async def show_venda(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> VendaModel | None:
    """
    Mostra uma venda existente.

    Parameters:
    id (int): O ID da venda a ser mostrada.

    Returns:
    Venda: A venda existente com o ID informado.
    """
    return db.query(VendaModel).filter(VendaModel.id == id_).first()


@venda_router.post(
    "/vendas",
    tags=[tag],
    name="venda_create",
    summary="Venda Create",
    description="Venda Create",
    response_description="Venda Create",
    status_code=201,
    response_model=VendaScherma,
)
async def create_venda(
    venda: VendaScherma, db: Annotated[Session, Depends(get_db)]
) -> VendaModel:
    """
    Cria uma nova venda.

    Parameters:
    venda (Venda): A venda a ser criada.

    Returns:
    Venda: A venda criada.
    """
    db_venda = VendaModel(**venda.model_dump())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


@venda_router.patch(
    "/vendas/{id}",
    tags=[tag],
    name="venda_update",
    summary="Venda Update",
    description="Venda Update",
    response_description="Venda Update",
    status_code=200,
    response_model=VendaScherma,
)
async def update_venda(
    id_: int, venda: VendaScherma, db: Annotated[Session, Depends(get_db)]
) -> VendaModel | None:
    """
    Atualiza uma venda existente.

    Parameters:
    id (int): O ID da venda a ser atualizada.
    venda (Venda): A venda com as informações atualizadas.

    Returns:
    Venda: A venda atualizada.
    """
    data = venda.model_dump(exclude_unset=True)
    stmt = (
        update(VendaModel)
        .where(VendaModel.id == id_)
        .values({getattr(VendaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(VendaModel).filter(VendaModel.id == id_).first()


@venda_router.delete(
    "/venda/{id}",
    tags=[tag],
    name="venda_delete",
    summary="Venda Delete",
    description="Venda Delete",
    response_description="Venda Delete",
    status_code=204,
)
async def delete_venda(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    """
    Remove uma venda pelo seu ID.

    Parameters:
    id (int): O ID da venda a ser removida.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(VendaModel).filter(VendaModel.id == id_).delete()
    db.commit()
    return JSONResponse("Venda removida com sucesso.", status_code=204)
