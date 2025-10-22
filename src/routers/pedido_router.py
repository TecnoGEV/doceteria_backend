from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import (
    ItemModel,
    PedidoModel,
)
from src.scherma import (
    ItemScherma,
    PedidoScherma,
)

pedido_router = APIRouter()
tag = "Pedido"

@pedido_router.get(
    "/pedidos",
    tags=[tag],
    name="pedido_index",
    summary="Pedido Index",
    description="Pedido Index",
    response_description="Pedido Index",
    status_code=200,
    response_model=list[PedidoScherma],
)
async def pedido_index(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> List[PedidoModel]:
    """Lista todos os pedidos cadastrados."""
    offset = (page - 1) * page_size
    receitas = db.query(PedidoModel).offset(offset).limit(page_size).all()
    return receitas


@pedido_router.get(
    "/pedido/{id}",
    tags=[tag],
    name="pedido_show",
    summary="Pedido Show",
    description="Pedido Show",
    response_description="Pedido Show",
    status_code=200,
    response_model=PedidoScherma,
)
async def show_pedido(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> PedidoModel | None:
    """
    Mostra um pedido existente.

    Parameters:
    id (int): O ID do pedido a ser mostrado.

    Returns:
    Pedido: O pedido existente com o ID informado.
    """
    return db.query(PedidoModel).filter(PedidoModel.id == id_).first()


@pedido_router.post(
    "/pedidos",
    tags=[tag],
    name="pedido_create",
    summary="Pedido Create",
    description="Pedido Create",
    response_description="Pedido Create",
    status_code=201,
    response_model=PedidoScherma,
)
async def create_pedido(
    pedido: PedidoScherma, db: Annotated[Session, Depends(get_db)]
) -> PedidoModel | None:
    """
    Cria um novo pedido.

    Parameters:
    pedido (Pedido): O pedido a ser criado.

    Returns:
    Pedido: O pedido criado.
    """
    model = {**pedido.model_dump()}

    model["preco_total"] = sum(
        item["preco_unitario"] * item["quantidade"] for item in model["itens_pedido"]
    )

    model["quantidade"] = model["itens_pedido"].__len__()

    db_pedido = PedidoModel(
        cliente_id=model["cliente_id"],
        preco_total=model["preco_total"],
        quantidade=model["quantidade"],
    )

    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    for item in model["itens_pedido"]:
        item_selecionado = ItemScherma(
            pedido_id=db_pedido.id,
            produto_id=item["produto_id"],
            quantidade=item["quantidade"],
            preco_unitario=item["preco_unitario"],
        )

        db_item = ItemModel(**item_selecionado.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

    pedido_model = db.query(PedidoModel).filter(PedidoModel.id == db_pedido.id).first()

    if pedido_model is None:
        return None
    return pedido_model


@pedido_router.delete(
    "/pedido/{id}",
    tags=[tag],
    name="pedido_delete",
    summary="Pedido Delete",
    description="Pedido Delete",
    response_description="Pedido Delete",
    status_code=204,
)
async def delete_pedido(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    """
    Remove um pedido pelo seu ID.

    Parameters:
    id (int): O ID do pedido a ser removido.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(PedidoModel).filter(PedidoModel.id == id_).delete()
    db.commit()
    return JSONResponse("Pedido removido com sucesso.", status_code=status.HTTP_200_OK)


@pedido_router.patch(
    "/pedidos/{id}",
    tags=[tag],
    name="pedido_update",
    summary="Pedido Update",
    description="Pedido Update",
    response_description="Pedido Update",
    status_code=200,
    response_model=PedidoScherma,
)
async def update_pedido(
    id_: int, pedido: PedidoScherma, db: Annotated[Session, Depends(get_db)]
) -> PedidoModel | None:
    """
    Atualiza um pedido existente.

    Parameters:
    id (int): O ID do pedido a ser atualizado.
    pedido (Pedido): O pedido com as informações atualizadas.

    Returns:
    Pedido: O pedido atualizado.
    """
    data = pedido.model_dump(exclude_unset=True)
    stmt = (
        update(PedidoModel)
        .where(PedidoModel.id == id_)
        .values({getattr(PedidoModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(PedidoModel).filter(PedidoModel.id == id_).first()
