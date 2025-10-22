from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import (
    CategoriaModel,
    ClienteModel,
    ItemModel,
    PedidoModel,
    ProdutoModel,
    ReceitaModel,
    VendaModel,
)
from src.scherma import (
    CategoriaScherma,
    ClienteScherma,
    ItemScherma,
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
) -> List[ReceitaModel]:
    """
    Retorna uma lista paginada de receitas.
    """
    offset = (page - 1) * page_size
    receitas = db.query(ReceitaModel).offset(offset).limit(page_size).all()
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
) -> ReceitaModel | None:
    """
    Mostra uma receita existente.

    Parameters:
    id (int): O ID da receita a ser mostrada.

    Returns:
    Receita: A receita existente com o ID informado.
    """
    return db.query(ReceitaModel).filter(ReceitaModel.id == id_).first()


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
    db.query(ReceitaModel).filter(ReceitaModel.id == id_).delete()
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
) -> list[ProdutoModel]:
    """Lista todos os produtos cadastrados."""
    offset = (page - 1) * page_size
    produtos = db.query(ProdutoModel).offset(offset).limit(page_size).all()
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
) -> ProdutoModel | None:
    """
    Mostra um produto existente.

    Parameters:
    id (int): O ID do produto a ser mostrado.

    Returns:
    Produto: O produto existente com o ID informado.
    """
    return db.query(ProdutoModel).filter(ProdutoModel.id == id_).first()


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
) -> ProdutoModel:
    """
    Cria um novo produto.

    Parameters:
    produto (Produto): O produto a ser criado.

    Returns:
    Produto: O produto criado.
    """

    model = { **produto.model_dump() }
    
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
    db.query(ProdutoModel).filter(ProdutoModel.id == id_).delete()
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
) -> list[VendaModel]:
    """Lista todas as vendas cadastradas."""
    offset = (page - 1) * page_size
    return db.query(VendaModel).offset(offset).limit(page_size).all()


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
    db.query(VendaModel).filter(VendaModel.id == id_).delete()
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
) -> list[PedidoModel]:
    """Lista todos os pedidos cadastrados."""
    offset = (page - 1) * page_size
    receitas = db.query(PedidoModel).offset(offset).limit(page_size).all()
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
) -> PedidoModel | None:
    """
    Mostra um pedido existente.

    Parameters:
    id (int): O ID do pedido a ser mostrado.

    Returns:
    Pedido: O pedido existente com o ID informado.
    """
    return db.query(PedidoModel).filter(PedidoModel.id == id_).first()


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
) -> PedidoModel | None:
    """
    Cria um novo pedido.

    Parameters:
    pedido (Pedido): O pedido a ser criado.

    Returns:
    Pedido: O pedido criado.
    """
    model = { **pedido.model_dump() }
    
    model['preco_total'] = sum(
        item['preco_unitario'] * item['quantidade'] 
        for item in model['itens_pedido']
    )
    
    model['quantidade'] = model['itens_pedido'].__len__()
    
    db_pedido = PedidoModel(
        cliente_id=model['cliente_id'],
        preco_total=model['preco_total'],
        quantidade=model['quantidade'],
    )

    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    for item in model['itens_pedido']:
        item_selecionado = ItemScherma(
            pedido_id=db_pedido.id,
            produto_id=item['produto_id'],
            quantidade=item['quantidade'],
            preco_unitario=item['preco_unitario'],
        )

        db_item = ItemModel(**item_selecionado.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
    pedido_model = db.query(PedidoModel).filter(PedidoModel.id == db_pedido.id).first()

    if pedido_model is None:
        return None
    return pedido_model

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
    db.query(PedidoModel).filter(PedidoModel.id == id_).delete()
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
) -> List[CategoriaModel]:
    """
    Retorna uma lista paginada de categorias.
    """
    offset = (page - 1) * page_size
    categorias = db.query(CategoriaModel).offset(offset).limit(page_size).all()
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
) -> CategoriaModel | None:
    """
    Mostra uma categoria existente.

    Parameters:
    id (int): O ID da categoria a ser mostrada.

    Returns:
    Categoria: A categoria existente com o ID informado.
    """
    return db.query(CategoriaModel).filter(CategoriaModel.id == id_).first()


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
    db.query(CategoriaModel).filter(CategoriaModel.id == id_).delete()
    db.commit()
    return JSONResponse("Categoria removida com sucesso.", status_code=204)


@router.get(
    "/clientes",
    tags=["cliente"],
    name="cliente_index",
    summary="Listar clientes",
    description="Retorna uma lista paginada de clientes.",
    response_description="Lista de clientes",
    status_code=status.HTTP_200_OK,
    response_model=List[ClienteScherma],
)
def listar_clientes(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> List[ClienteModel]:
    offset = (page - 1) * page_size
    clientes = db.query(ClienteModel).offset(offset).limit(page_size).all()
    return clientes


@router.post(
    "/clientes",
    tags=["cliente"],
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


@router.get(
    "/clientes/{id}",
    tags=["cliente"],
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


@router.patch(
    "/clientes/{id}",
    tags=["cliente"],
    name="cliente_update",
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente.",
    response_description="Cliente atualizado com sucesso.",
    status_code=status.HTTP_200_OK,
    response_model=ClienteScherma,
)
def atualizar_cliente(
    id_: int, cliente_data: ClienteScherma, db: Annotated[Session, Depends(get_db)]
) -> ClienteModel:
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    for key, value in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete(
    "/clientes/{id}",
    tags=["cliente"],
    name="cliente_destroy",
    summary="Excluir cliente",
    description="Remove um cliente do sistema.",
    response_description="Cliente excluído com sucesso.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deletar_cliente(id_: int, db: Annotated[Session, Depends(get_db)]):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id_).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    db.delete(cliente)
    db.commit()
    return None
