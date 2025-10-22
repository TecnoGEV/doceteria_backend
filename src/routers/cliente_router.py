from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import ClienteModel
from src.scherma import ClienteScherma

cliente_router = APIRouter()
tag = "Cliente"


@cliente_router.get(
    "/clientes",
    tags=[tag],
    name="cliente_index",
    summary="Listar clientes",
    description="Retorna uma lista paginada de clientes.",
    response_description="Lista de clientes",
    status_code=status.HTTP_200_OK,
    response_model=list[ClienteScherma],
)
def listar_clientes(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> list[ClienteModel]:
    offset = (page - 1) * page_size
    clientes = db.query(ClienteModel).offset(offset).limit(page_size).all()
    return clientes


@cliente_router.post(
    "/clientes",
    tags=[tag],
    name="cliente_store",
    summary="Criar cliente",
    description="Cria um novo cliente no sistema.",
    response_description="Cliente criado com sucesso.",
    status_code=status.HTTP_201_CREATED,
    response_model=ClienteScherma,
)
def criar_cliente(
    cliente: ClienteScherma, db: Annotated[Session, Depends(get_db)]
) -> ClienteModel:
    novo_cliente = ClienteModel(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente


@cliente_router.get(
    "/clientes/{id}",
    tags=[tag],
    name="cliente_show",
    summary="Mostrar cliente",
    description="Retorna um cliente específico pelo ID.",
    response_description="Cliente retornado com sucesso.",
    status_code=status.HTTP_200_OK,
    response_model=ClienteScherma,
)
def mostrar_cliente(id_: int, db: Annotated[Session, Depends(get_db)]) -> ClienteModel:
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id_).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@cliente_router.patch(
    "/clientes/{id}",
    tags=[tag],
    name="cliente_update",
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente.",
    response_description="Cliente atualizado com sucesso.",
    status_code=status.HTTP_200_OK,
    response_model=ClienteScherma,
)
def atualizar_cliente(
    id_: int,
    cliente_data: ClienteScherma,
    db: Annotated[Session, Depends(get_db)],
) -> ClienteModel:
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    for key, value in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


@cliente_router.delete(
    "/clientes/{id}",
    tags=[tag],
    name="cliente_destroy",
    summary="Excluir cliente",
    description="Remove um cliente do sistema.",
    response_description="Cliente excluído com sucesso.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_cliente(id_: int, db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id_).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    db.delete(cliente)
    db.commit()
    return JSONResponse(
        content={"message": "Cliente excluído com sucesso."},
        status_code=status.HTTP_204_NO_CONTENT,
    )
