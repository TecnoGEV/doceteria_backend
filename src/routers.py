from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import update
from config.database import SessionLocal
from src.scherma import (
    ReceitaScherma, ProdutoScherma,
    VendaScherma, PedidoScherma, CategoriaScherma
)
from src.models import (
    Produto as ProdutoModel, Receita as ReceitaModel,
    Venda as VendaModel, Pedido as PedidoModel, Categoria as CategoriaModel
)
router = APIRouter()

def get_db():
    """
    Generator for database sessions.

    Yields a database session object and closes it when the generator is exited.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/",
    tags=["receita"],
    name="receita_index",
    summary="Receita Index",
    description="Receita Index",
    response_description="Receita Index",
    status_code=200,
    response_model=List[ReceitaScherma],
    )
async def receita_index(db: Session = Depends(get_db)) -> List[ReceitaModel]:
    """Lista todas as receitas cadastradas."""
    return db.query(ReceitaModel).all()


@router.post("/",
    tags=["receita"],
    name="receita_create",
    summary="Receita Create",
    description="Receita Create",
    response_description="Receita Create",
    status_code=201,
    response_model=ReceitaScherma,
    )
async def create_receita(receita: ReceitaScherma, db: Session = Depends(get_db)) -> ReceitaModel:
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


@router.get("/{id}", 
    tags=["receita"],
    name="receita_show",
    summary="Receita Show",
    description="Receita Show",
    response_description="Receita Show",
    status_code=200,
    response_model=ReceitaScherma,
    )
async def show_receita(id: int, db: Session = Depends(get_db)) -> (ReceitaModel | None):
    """
    Mostra uma receita existente.

    Parameters:
    id (int): O ID da receita a ser mostrada.

    Returns:
    Receita: A receita existente com o ID informado.
    """
    return db.query(ReceitaModel).filter(ReceitaModel.id == id).first()


@router.patch("/{id}",
    tags=["receita"],
    name="receita_update",
    summary="Receita Update",
    description="Receita Update",
    response_description="Receita Update",
    status_code=200,
    response_model=ReceitaScherma,
    )
async def update_receita(id: int, receita: ReceitaScherma, db: Session = Depends(get_db))-> ReceitaModel | None:
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
        .where(ReceitaModel.id == id)
        .values({getattr(ReceitaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(ReceitaModel).filter(ReceitaModel.id == id).first()


@router.delete("/{id}",
    tags=["receita"],
    name="receita_delete",
    summary="Receita Delete",
    description="Receita Delete",
    response_description="Receita Delete",
    status_code=204,
)
async def delete_receita(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Remove uma receita pelo seu ID.

    Parameters:
    id (int): O ID da receita a ser removida.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(ReceitaModel).filter(ReceitaModel.id == id).delete()
    db.commit()
    return JSONResponse("Receita removida com sucesso.",status_code=204)


@router.get("/produtos",
    tags=["produto"],
    name="produto_index",
    summary="Produto Index",
    description="Produto Index",
    response_description="Produto Index",
    status_code=200,
    response_model=List[ProdutoScherma],
    )
async def produto_index(db: Session = Depends(get_db)) -> List[ProdutoModel]:
    """Lista todos os produtos cadastrados."""
    return db.query(ProdutoModel).all()

@router.get("/produtos/{id}",
    tags=["produto"],
    name="produto_show",
    summary="Produto Show",
    description="Produto Show",
    response_description="Produto Show",
    status_code=200,
    response_model=ProdutoScherma,
    )
async def show_produto(id: int, db: Session = Depends(get_db)) -> (ProdutoModel | None):
    """
    Mostra um produto existente.

    Parameters:
    id (int): O ID do produto a ser mostrado.

    Returns:
    Produto: O produto existente com o ID informado.
    """
    return db.query(ProdutoModel).filter(ProdutoModel.id == id).first()

@router.post("/produtos",
    tags=["produto"],
    name="produto_create",
    summary="Produto Create",
    description="Produto Create",
    response_description="Produto Create",
    status_code=201,
    response_model=ProdutoScherma,
    )
async def create_produto(produto: ProdutoScherma, db: Session = Depends(get_db)) -> ProdutoModel:
    """
    Cria um novo produto.

    Parameters:
    produto (Produto): O produto a ser criado.

    Returns:
    Produto: O produto criado.
    """
    db_produto = ProdutoModel(**produto.model_dump())
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
async def update_produto(id: int, produto: ProdutoScherma, db: Session = Depends(get_db)) -> (ProdutoModel | None):
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
        .where(ProdutoModel.id == id)
        .values({getattr(ProdutoModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(ProdutoModel).filter(ProdutoModel.id == id).first()

@router.delete("/{id}",
    tags=["produto"],
    name="produto_delete",
    summary="Produto Delete",
    description="Produto Delete",
    response_description="Produto Delete",
    status_code=204,
)
async def delete_produto(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Remove um produto pelo seu ID.

    Parameters:
    id (int): O ID do produto a ser removido.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(ProdutoModel).filter(ProdutoModel.id == id).delete()
    db.commit()
    return JSONResponse("Produto removido com sucesso.",status_code=204)

@router.get("/vendas",
    tags=["venda"],
    name="venda_index",
    summary="Venda Index",
    description="Venda Index",
    response_description="Venda Index",
    status_code=200,
    response_model=List[VendaScherma],
    )
async def venda_index(db: Session = Depends(get_db)) -> List[VendaModel]:
    """Lista todas as vendas cadastradas."""
    return db.query(VendaModel).all()

@router.get("/venda/{id}",
    tags=["venda"],
    name="venda_show",
    summary="Venda Show",
    description="Venda Show",
    response_description="Venda Show",
    status_code=200,
    response_model=VendaScherma,
    )
async def show_venda(id: int, db: Session = Depends(get_db)) -> (VendaModel | None):
    """
    Mostra uma venda existente.

    Parameters:
    id (int): O ID da venda a ser mostrada.

    Returns:
    Venda: A venda existente com o ID informado.
    """
    return db.query(VendaModel).filter(VendaModel.id == id).first()

@router.post("/vendas",
    tags=["venda"],
    name="venda_create",
    summary="Venda Create",
    description="Venda Create",
    response_description="Venda Create",
    status_code=201,
    response_model=VendaScherma,
    )
async def create_venda(venda: VendaScherma, db: Session = Depends(get_db)) -> VendaModel:
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
async def update_venda(id: int, venda: VendaScherma, db: Session = Depends(get_db)) -> (VendaModel | None):
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
        .where(VendaModel.id == id)
        .values({getattr(VendaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(VendaModel).filter(VendaModel.id == id).first()

@router.delete("/{id}",
    tags=["venda"],
    name="venda_delete",
    summary="Venda Delete",
    description="Venda Delete",
    response_description="Venda Delete",
    status_code=204,
)
async def delete_venda(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Remove uma venda pelo seu ID.

    Parameters:
    id (int): O ID da venda a ser removida.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(VendaModel).filter(VendaModel.id == id).delete()
    db.commit()
    return JSONResponse("Venda removida com sucesso.",status_code=204)

@router.get("/pedidos",
    tags=["pedido"],
    name="pedido_index",
    summary="Pedido Index",
    description="Pedido Index",
    response_description="Pedido Index",
    status_code=200,
    response_model=List[PedidoScherma],
    )
async def pedido_index(db: Session = Depends(get_db)) -> List[PedidoModel]:
    """Lista todos os pedidos cadastrados."""
    return db.query(PedidoModel).all()

@router.get("/pedido/{id}",
    tags=["pedido"],
    name="pedido_show",
    summary="Pedido Show",
    description="Pedido Show",
    response_description="Pedido Show",
    status_code=200,
    response_model=PedidoScherma,
    )
async def show_pedido(id: int, db: Session = Depends(get_db)) -> (PedidoModel | None):
    """
    Mostra um pedido existente.

    Parameters:
    id (int): O ID do pedido a ser mostrado.

    Returns:
    Pedido: O pedido existente com o ID informado.
    """
    return db.query(PedidoModel).filter(PedidoModel.id == id).first()

@router.post("/pedidos",
    tags=["pedido"],
    name="pedido_create",
    summary="Pedido Create",
    description="Pedido Create",
    response_description="Pedido Create",
    status_code=201,
    response_model=PedidoScherma,
    )
async def create_pedido(pedido: PedidoScherma, db: Session = Depends(get_db)) -> PedidoModel:
    """
    Cria um novo pedido.

    Parameters:
    pedido (Pedido): O pedido a ser criado.

    Returns:
    Pedido: O pedido criado.
    """
    db_pedido = PedidoModel(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.delete("/{id}",
    tags=["pedido"],
    name="pedido_delete",
    summary="Pedido Delete",
    description="Pedido Delete",
    response_description="Pedido Delete",
    status_code=204,
)
async def delete_pedido(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Remove um pedido pelo seu ID.

    Parameters:
    id (int): O ID do pedido a ser removido.

    Returns:
    JSONResponse: Uma resposta JSON com uma mensagem de sucesso e status code 204.
    """
    db.query(PedidoModel).filter(PedidoModel.id == id).delete()
    db.commit()
    return JSONResponse("Pedido removido com sucesso.",status_code=204)

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
async def update_pedido(id: int, pedido: PedidoScherma, db: Session = Depends(get_db)) -> PedidoModel | None:
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
        .where(PedidoModel.id == id)
        .values({getattr(PedidoModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(PedidoModel).filter(PedidoModel.id == id).first()

@router.get('/categorias',
    tags=['categoria'],
    name='categoria_index',
    summary='Categoria Index',
    description='Categoria Index',
    response_description='Categoria Index',
    status_code=200,
    response_model=List[CategoriaScherma],
    )
async def categoria_index(db: Session = Depends(get_db)) -> List[CategoriaModel]:
    """Lista todas as categorias cadastradas."""
    return db.query(CategoriaModel).all()

@router.get('/categoria/{id}',
    tags=['categoria'],
    name='categoria_show',
    summary='Categoria Show',
    description='Categoria Show',
    response_description='Categoria Show',
    status_code=200,
    response_model=CategoriaScherma,
    )
async def show_categoria(id: int, db: Session = Depends(get_db)) -> (CategoriaModel | None):
    """
    Mostra uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser mostrada.

    Returns:
    Categoria: A categoria existente com o ID informado.
    """
    return db.query(CategoriaModel).filter(CategoriaModel.id == id).first()

@router.post('/categorias',
    tags=['categoria'],
    name='categoria_create',
    summary='Categoria Create',
    description='Categoria Create',
    response_description='Categoria Create',
    status_code=201,
    response_model=CategoriaScherma,
    )
async def create_categoria(categoria: CategoriaScherma, db: Session = Depends(get_db)) -> CategoriaModel:
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

@router.patch(
    "/categorias/{id}",
    tags=["categoria"],
    name="categoria_update",
    summary="Categoria Update",
    description="Categoria Update",
    response_description="Categoria Update",
    status_code=200,
    response_model=CategoriaScherma,
)
async def update_categoria(id: int, categoria: CategoriaScherma, db: Session = Depends(get_db)) -> CategoriaModel | None:
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
        .where(CategoriaModel.id == id)
        .values({getattr(CategoriaModel, k): v for k, v in data.items()})
    )
    db.execute(stmt)
    db.commit()
    return db.query(CategoriaModel).filter(CategoriaModel.id == id).first()

@router.delete('/categorias/{id}',
    tags=['categoria'],
    name='categoria_delete',
    summary='Categoria Delete',
    description='Categoria Delete',
    response_description='Categoria Delete',
    status_code=204,
    )
async def delete_categoria(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Deleta uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser deletada.

    Returns:
    JSONResponse: Uma resposta JSON com o código de status 204.
    """
    db.query(CategoriaModel).filter(CategoriaModel.id == id).delete()
    db.commit()
    return JSONResponse('Categoria removida com sucesso.',status_code=204)
