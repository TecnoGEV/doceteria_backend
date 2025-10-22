from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import (
    ProdutoModel,
)
from src.scherma import (
    ProdutoScherma,
)

produto_router = APIRouter()
tag = "Produto"

@produto_router.get(
    "/produtos",
    tags=[tag],
    name="produto_index",
    summary="Produto Index",
    description="Produto Index",
    response_description="Produto Index",
    status_code=200,
    response_model=List[ProdutoScherma],
)
async def produto_index(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> List[ProdutoModel]:
    """Lista todos os produtos cadastrados."""
    offset = (page - 1) * page_size
    produtos = db.query(ProdutoModel).offset(offset).limit(page_size).all()
    return produtos


@produto_router.get(
    "/produtos/{id}",
    tags=[tag],
    name="produto_show",
    summary="Produto Show",
    description="Produto Show",
    response_description="Produto Show",
    status_code=200,
    response_model=ProdutoScherma,
)
async def show_produto(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> ProdutoModel | None:
    """
    Mostra um produto existente.

    Parameters:
    id (int): O ID do produto a ser mostrado.

    Returns:
    Produto: O produto existente com o ID informado.
    """
    return db.query(ProdutoModel).filter(ProdutoModel.id == id_).first()


@produto_router.post(
    "/produtos",
    tags=[tag],
    name="produto_create",
    summary="Produto Create",
    description="Produto Create",
    response_description="Produto Create",
    status_code=201,
    response_model=ProdutoScherma,
)
async def create_produto(
    produto: ProdutoScherma, db: Annotated[Session, Depends(get_db)]
) -> ProdutoModel:
    """
    Cria um novo produto.

    Parameters:
    produto (Produto): O produto a ser criado.

    Returns:
    Produto: O produto criado.
    """

    model = {**produto.model_dump()}

    db_produto = ProdutoModel(
        nome_produto=model["nome_produto"],
        data_validade=model["data_validade"],
        marca=model["marca"],
        codigo_barras=model["codigo_barras"],
        preco_unidade=model["preco_unidade"],
        unidade=model["unidade"],
        quantidade=model["quantidade"],
        categoria_id=model["categoria_id"],
    )

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)

    return db_produto


@produto_router.patch(
    "/produtos/{id}",
    tags=[tag],
    name="produto_update",
    summary="Produto Update",
    description="Produto Update",
    response_description="Produto Update",
    status_code=200,
    response_model=ProdutoScherma,
)
async def update_produto(
    id_: int, produto: ProdutoScherma, db: Annotated[Session, Depends(get_db)]
) -> ProdutoModel | None:
    """
    Atualiza um produto existente.

    Parameters:
    id (int): O ID do produto a ser atualizado.
    produto (Produto): O produto com as informações atualizadas.

    Returns:
    Produto: O produto atualizado.
    """

    data = produto.model_dump(exclude_unset=True)
    stmt = (
        update(ProdutoModel)
        .where(ProdutoModel.id == id_)
        .values({getattr(ProdutoModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(ProdutoModel).filter(ProdutoModel.id == id_).first()


@produto_router.delete(
    "/{id}",
    tags=[tag],
    name="produto_delete",
    summary="Produto Delete",
    description="Produto Delete",
    response_description="Produto Delete",
    status_code=204,
)
async def delete_produto(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    """
    Remove um produto pelo seu ID.

    Parameters:
    id (int): O ID do produto a ser removido.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(ProdutoModel).filter(ProdutoModel.id == id_).delete()
    db.commit()
    return JSONResponse("Produto removido com sucesso.", status_code=204)
