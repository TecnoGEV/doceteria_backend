from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models.categoria_model import CategoriaModel
from src.schermas.categoria_scherma import CategoriaScherma

categoria_router = APIRouter()
tag = "Categoria"


@categoria_router.get("/", include_in_schema=False)
def read_root():
    return {"message": "Hello World"}


@categoria_router.get(
    "/categorias",
    tags=[tag],
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
) -> list[CategoriaModel]:
    """
    Retorna uma lista paginada de categorias.
    """
    offset = (page - 1) * page_size
    categorias = db.query(CategoriaModel).offset(offset).limit(page_size).all()
    return categorias


@categoria_router.get(
    "/categoria/{id}",
    tags=[tag],
    name="categoria_show",
    summary="Categoria Show",
    description="Categoria Show",
    response_description="Categoria Show",
    status_code=200,
    response_model=CategoriaScherma,
)
async def show_categoria(
    id_: int, db: Annotated[Session, Depends(get_db)]
) -> CategoriaModel | None:
    """
    Mostra uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser mostrada.

    Returns:
    Categoria: A categoria existente com o ID informado.
    """
    return db.query(CategoriaModel).filter(CategoriaModel.id == id_).first()


@categoria_router.post(
    "/categorias",
    tags=[tag],
    name="categoria_create",
    summary="Categoria Create",
    description="Categoria Create",
    response_description="Categoria Create",
    status_code=201,
    response_model=CategoriaScherma,
)
async def create_categoria(
    categoria: CategoriaScherma, db: Annotated[Session, Depends(get_db)]
) -> CategoriaModel:
    """
    Cria uma nova categoria.

    Parameters:
    categoria (Categoria): A categoria a ser criada.

    Returns:
    Categoria: A categoria criada.
    """
    db_categoria = CategoriaModel(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@categoria_router.patch(
    "/categoria/{id}",
    tags=[tag],
    name="categoria_update",
    summary="Categoria Update",
    description="Categoria Update",
    response_description="Categoria Update",
    status_code=200,
    response_model=CategoriaScherma,
)
async def update_categoria(
    id_: int,
    categoria: CategoriaScherma,
    db: Annotated[Session, Depends(get_db)],
) -> CategoriaModel | None:
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
        update(CategoriaModel)
        .where(CategoriaModel.id == id_)
        .values({getattr(CategoriaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(CategoriaModel).filter(CategoriaModel.id == id_).first()


@categoria_router.delete(
    "/categoria/{id}",
    tags=[tag],
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
    db.query(CategoriaModel).filter(CategoriaModel.id == id_).delete()
    db.commit()
    return JSONResponse("Categoria removida com sucesso.", status_code=204)
