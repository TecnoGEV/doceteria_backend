from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import Categoria, Pedido, Produto, Receita, Venda
from src.scherma import (
    CategoriaScherma,
    PedidoScherma,
    ProdutoScherma,
    ReceitaScherma,
    VendaScherma,
)

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello World"}


@router.get(
    "/receitas",
    tags=["receita"],
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
):
    """
    Retorna uma lista paginada de receitas.
    """
    offset = (page - 1) * page_size
    receitas = db.query(Receita).offset(offset).limit(page_size).all()
    return receitas


@router.post(
    "/receitas",
    tags=["receita"],
    name="receita_create",
    summary="Receita Create",
    description="Receita Create",
    response_description="Receita Create",
    status_code=201,
    response_model=ReceitaScherma,
)
async def create_receita(
    receita: ReceitaScherma, db: Annotated[Session, Depends(get_db)]
) -> Receita:
    """
    Cria uma nova receita.

    Parameters:
    receita (Receita): Receita a ser criada.

    Returns:
    Receita: A nova receita criada.
    """
    db_receita = Receita(**receita.model_dump())
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita


@router.get(
    "/receita/{id}",
    tags=["receita"],
    name="receita_show",
    summary="Receita Show",
    description="Receita Show",
    response_description="Receita Show",
    status_code=200,
    response_model=ReceitaScherma,
)
async def show_receita(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> Receita | None:
    """
    Mostra uma receita existente.

    Parameters:
    id (int): O ID da receita a ser mostrada.

    Returns:
    Receita: A receita existente com o ID informado.
    """
    return db.query(Receita).filter(Receita.id == id_).first()


@router.patch(
    "/receita/{id}",
    tags=["receita"],
    name="receita_update",
    summary="Receita Update",
    description="Receita Update",
    response_description="Receita Update",
    status_code=200,
    response_model=ReceitaScherma,
)
async def update_receita(
    id_: int, receita: ReceitaScherma, db: Annotated[Session, Depends(get_db)]
) -> Receita | None:
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
        update(Receita)
        .where(Receita.id == id_)
        .values({getattr(Receita, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(Receita).filter(Receita.id == id_).first()


@router.delete(
    "/receita/{id}",
    tags=["receita"],
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
    db.query(Receita).filter(Receita.id == id_).delete()
    db.commit()
    return JSONResponse("Receita removida com sucesso.", status_code=204)


@router.get(
    "/produtos",
    tags=["produto"],
    name="produto_index",
    summary="Produto Index",
    description="Produto Index",
    response_description="Produto Index",
    status_code=200,
    response_model=list[ProdutoScherma],
)
async def produto_index(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> list[Produto]:
    """Lista todos os produtos cadastrados."""
    offset = (page - 1) * page_size
    produtos = db.query(Produto).offset(offset).limit(page_size).all()
    return produtos


@router.get(
    "/produtos/{id}",
    tags=["produto"],
    name="produto_show",
    summary="Produto Show",
    description="Produto Show",
    response_description="Produto Show",
    status_code=200,
    response_model=ProdutoScherma,
)
async def show_produto(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> Produto | None:
    """
    Mostra um produto existente.

    Parameters:
    id (int): O ID do produto a ser mostrado.

    Returns:
    Produto: O produto existente com o ID informado.
    """
    return db.query(Produto).filter(Produto.id == id_).first()


@router.post(
    "/produtos",
    tags=["produto"],
    name="produto_create",
    summary="Produto Create",
    description="Produto Create",
    response_description="Produto Create",
    status_code=201,
    response_model=ProdutoScherma,
)
async def create_produto(
    produto: ProdutoScherma, db: Annotated[Session, Depends(get_db)]
) -> Produto:
    """
    Cria um novo produto.

    Parameters:
    produto (Produto): O produto a ser criado.

    Returns:
    Produto: O produto criado.
    """
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.patch(
    "/produtos/{id}",
    tags=["produto"],
    name="produto_update",
    summary="Produto Update",
    description="Produto Update",
    response_description="Produto Update",
    status_code=200,
    response_model=ProdutoScherma,
)
async def update_produto(
    id_: int, produto: ProdutoScherma, db: Annotated[Session, Depends(get_db)]
) -> Produto | None:
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
        update(Produto)
        .where(Produto.id == id_)
        .values({getattr(Produto, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(Produto).filter(Produto.id == id_).first()


@router.delete(
    "/{id}",
    tags=["produto"],
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
    db.query(Produto).filter(Produto.id == id_).delete()
    db.commit()
    return JSONResponse("Produto removido com sucesso.", status_code=204)


@router.get(
    "/vendas",
    tags=["venda"],
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
) -> list[Venda]:
    """Lista todas as vendas cadastradas."""
    offset = (page - 1) * page_size
    return db.query(Venda).offset(offset).limit(page_size).all()


@router.get(
    "/venda/{id}",
    tags=["venda"],
    name="venda_show",
    summary="Venda Show",
    description="Venda Show",
    response_description="Venda Show",
    status_code=200,
    response_model=VendaScherma,
)
async def show_venda(id_: int, db: Annotated[Session, Depends(get_db)]) -> Venda | None:
    """
    Mostra uma venda existente.

    Parameters:
    id (int): O ID da venda a ser mostrada.

    Returns:
    Venda: A venda existente com o ID informado.
    """
    return db.query(Venda).filter(Venda.id == id_).first()


@router.post(
    "/vendas",
    tags=["venda"],
    name="venda_create",
    summary="Venda Create",
    description="Venda Create",
    response_description="Venda Create",
    status_code=201,
    response_model=VendaScherma,
)
async def create_venda(
    venda: VendaScherma, db: Annotated[Session, Depends(get_db)]
) -> Venda:
    """
    Cria uma nova venda.

    Parameters:
    venda (Venda): A venda a ser criada.

    Returns:
    Venda: A venda criada.
    """
    db_venda = Venda(**venda.model_dump())
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


@router.patch(
    "/vendas/{id}",
    tags=["venda"],
    name="venda_update",
    summary="Venda Update",
    description="Venda Update",
    response_description="Venda Update",
    status_code=200,
    response_model=VendaScherma,
)
async def update_venda(
    id_: int, venda: VendaScherma, db: Annotated[Session, Depends(get_db)]
) -> Venda | None:
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
        update(Venda)
        .where(Venda.id == id_)
        .values({getattr(Venda, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(Venda).filter(Venda.id == id_).first()


@router.delete(
    "/{id}",
    tags=["venda"],
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
    db.query(Venda).filter(Venda.id == id_).delete()
    db.commit()
    return JSONResponse("Venda removida com sucesso.", status_code=204)


@router.get(
    "/pedidos",
    tags=["pedido"],
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
) -> list[Pedido]:
    """Lista todos os pedidos cadastrados."""
    offset = (page - 1) * page_size
    receitas = db.query(Pedido).offset(offset).limit(page_size).all()
    return receitas


@router.get(
    "/pedido/{id}",
    tags=["pedido"],
    name="pedido_show",
    summary="Pedido Show",
    description="Pedido Show",
    response_description="Pedido Show",
    status_code=200,
    response_model=PedidoScherma,
)
async def show_pedido(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> Pedido | None:
    """
    Mostra um pedido existente.

    Parameters:
    id (int): O ID do pedido a ser mostrado.

    Returns:
    Pedido: O pedido existente com o ID informado.
    """
    return db.query(Pedido).filter(Pedido.id == id_).first()


@router.post(
    "/pedidos",
    tags=["pedido"],
    name="pedido_create",
    summary="Pedido Create",
    description="Pedido Create",
    response_description="Pedido Create",
    status_code=201,
    response_model=PedidoScherma,
)
async def create_pedido(
    pedido: PedidoScherma, db: Annotated[Session, Depends(get_db)]
) -> Pedido:
    """
    Cria um novo pedido.

    Parameters:
    pedido (Pedido): O pedido a ser criado.

    Returns:
    Pedido: O pedido criado.
    """
    db_pedido = Pedido(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.delete(
    "/pedido/{id}",
    tags=["pedido"],
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
    db.query(Pedido).filter(Pedido.id == id_).delete()
    db.commit()
    return JSONResponse("Pedido removido com sucesso.", status_code=204)


@router.patch(
    "/pedidos/{id}",
    tags=["pedido"],
    name="pedido_update",
    summary="Pedido Update",
    description="Pedido Update",
    response_description="Pedido Update",
    status_code=200,
    response_model=PedidoScherma,
)
async def update_pedido(
    id_: int, pedido: PedidoScherma, db: Annotated[Session, Depends(get_db)]
) -> Pedido | None:
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
        update(Pedido)
        .where(Pedido.id == id_)
        .values({getattr(Pedido, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(Pedido).filter(Pedido.id == id_).first()


@router.get(
    "/categorias",
    tags=["categoria"],
    name="categoria_index",
    summary="Categoria Index",
    description="Categoria Index",
    response_description="Categoria Index",
    status_code=200,
    response_model=list[CategoriaScherma],
)
def listar_categorias(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """
    Retorna uma lista paginada de receitas.
    """
    offset = (page - 1) * page_size
    categorias = db.query(Categoria).offset(offset).limit(page_size).all()
    return categorias


@router.get(
    "/categoria/{id}",
    tags=["categoria"],
    name="categoria_show",
    summary="Categoria Show",
    description="Categoria Show",
    response_description="Categoria Show",
    status_code=200,
    response_model=CategoriaScherma,
)
async def show_categoria(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> Categoria | None:
    """
    Mostra uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser mostrada.

    Returns:
    Categoria: A categoria existente com o ID informado.
    """
    return db.query(Categoria).filter(Categoria.id == id_).first()


@router.post(
    "/categorias",
    tags=["categoria"],
    name="categoria_create",
    summary="Categoria Create",
    description="Categoria Create",
    response_description="Categoria Create",
    status_code=201,
    response_model=CategoriaScherma,
)
async def create_categoria(
    categoria: CategoriaScherma, db: Annotated[Session, Depends(get_db)]
) -> Categoria:
    """
    Cria uma nova categoria.

    Parameters:
    categoria (Categoria): A categoria a ser criada.

    Returns:
    Categoria: A categoria criada.
    """
    db_categoria = Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.patch(
    "/categoria/{id}",
    tags=["categoria"],
    name="categoria_update",
    summary="Categoria Update",
    description="Categoria Update",
    response_description="Categoria Update",
    status_code=200,
    response_model=CategoriaScherma,
)
async def update_categoria(
    id_: int, categoria: CategoriaScherma, db: Annotated[Session, Depends(get_db)]
) -> Categoria | None:
    """
    Atualiza uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser atualizada.
    categoria (Categoria): A categoria com as informações atualizadas.

    Returns:
    Categoria: A categoria atualizada.
    """
    data = categoria.model_dump(exclude_unset=True)
    stmt = (
        update(Categoria)
        .where(Categoria.id == id_)
        .values({getattr(Categoria, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(Categoria).filter(Categoria.id == id_).first()


@router.delete(
    "/categoria/{id}",
    tags=["categoria"],
    name="categoria_delete",
    summary="Categoria Delete",
    description="Categoria Delete",
    response_description="Categoria Delete",
    status_code=204,
)
async def delete_categoria(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    """
    Deleta uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser deletada.

    Returns:
    JSONResponse: Uma resposta JSON com o código de status 204.
    """
    db.query(Categoria).filter(Categoria.id == id_).delete()
    db.commit()
    return JSONResponse("Categoria removida com sucesso.", status_code=204)
