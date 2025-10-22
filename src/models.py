from typing import List

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarativa moderna (SQLAlchemy 2.0)"""

    pass


# 🔗 Tabela associativa entre Receita e Ingrediente
receita_ingrediente_table = Table(
    "receita_ingrediente",
    Base.metadata,
    Column("receita_id", Integer, ForeignKey("receitas.id"), primary_key=True),
    Column("ingrediente_id", Integer, ForeignKey("ingredientes.id"), primary_key=True),
)


class ClienteModel(Base):
    """
    Classe que representa um cliente na doceteria.

    Attributes:
        id (int): O ID do cliente.
        nome (str): O nome do cliente.
        telefone (str): O telefone do cliente.
        endereco (str): O endereço do cliente.
    """

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)

    class Config:
        from_attributes = True


class IngredienteModel(Base):
    """
    Classe que representa um ingrediente na doceteria.

    Attributes:
        id (int): O ID do ingrediente.
        nome (str): O nome do ingrediente.
        receitas (List[Receita]): A lista de receitas que usam o ingrediente.
    """

    __tablename__ = "ingredientes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    # Relação inversa com Receita
    receitas: Mapped[list["ReceitaModel"]] = relationship(
        "ReceitaModel",
        secondary=receita_ingrediente_table,
        back_populates="ingredientes",
    )


class ReceitaModel(Base):
    """
    Classe que representa uma receita na doceteria.
    Attributes:
        id (int): O ID da receita.
        nome_receita (str): O nome da receita.
        porcao_rendimento (str): A porção de rendimento da receita.
        modo_preparo (str): O modo de preparo da receita.
        margem_lucro (float): A margem de lucro da receita.
        preco_sugerido (float): O preço sugerido da receita.
        preco_venda (float): O preço de venda da receita.
        custo_porcao (float): O custo por porção da receita.
        custo_total (float): O custo total da receita.
        lucro_sugerido (float): O lucro sugerido da receita.
        ingredientes (List[Ingrediente]): A lista de ingredientes usados na receita.
    """

    __tablename__ = "receitas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_receita: Mapped[str] = mapped_column(String(150))
    porcao_rendimento: Mapped[str] = mapped_column(String(50))
    modo_preparo: Mapped[str] = mapped_column(String)
    margem_lucro: Mapped[float] = mapped_column(Float)
    preco_sugerido: Mapped[float] = mapped_column(Float)
    preco_venda: Mapped[float] = mapped_column(Float)
    custo_porcao: Mapped[float] = mapped_column(Float)
    custo_porcao: Mapped[float] = mapped_column(Float)
    custo_total: Mapped[float] = mapped_column(Float)
    lucro_sugerido: Mapped[float] = mapped_column(Float)

    # Relação Many-to-Many com Ingredientes
    ingredientes: Mapped[list["IngredienteModel"]] = relationship(
        "IngredienteModel",
        secondary=receita_ingrediente_table,
        back_populates="receitas",
    )


# -------------------------------
# Categoria
# -------------------------------
class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)

    produtos: Mapped[list["ProdutoModel"]] = relationship(
        "ProdutoModel", back_populates="categoria"
    )


# -------------------------------
# Produto
# -------------------------------
class ProdutoModel(Base):

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_produto: Mapped[str] = mapped_column(String(150), nullable=False)
    data_validade: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_barras: Mapped[str] = mapped_column(String(50), unique=True)
    preco_unidade: Mapped[float] = mapped_column(Float, nullable=False)
    unidade: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[float] = mapped_column(Float, nullable=False)

    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel", back_populates="produtos"
    )

    itens: Mapped[List["ItemModel"]] = relationship(
        "ItemModel", back_populates="produto"
    )


# -------------------------------
# Pedido
# -------------------------------
class PedidoModel(Base):

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_total: Mapped[float] = mapped_column(Float, nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

    cliente: Mapped["ClienteModel"] = relationship("ClienteModel")

    itens_pedido = relationship(
        "ItemModel", back_populates="pedido", cascade="all, delete"
    )

    # 🔗 Relacionamento 1:1 com Venda
    venda: Mapped["VendaModel"] = relationship(
        "VendaModel",
        back_populates="pedido",
        uselist=False,  # garante 1:1
        cascade="all, delete-orphan",
    )


# -------------------------------
# Venda
# -------------------------------
class VendaModel(Base):

    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), unique=True)
    forma_pagamento: Mapped[str] = mapped_column(String(50), nullable=False)
    status_venda: Mapped[str] = mapped_column(String(50), nullable=False)

    pedido: Mapped["PedidoModel"] = relationship("PedidoModel", back_populates="venda")


class ItemModel(Base):

    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    quantidade: Mapped[float] = mapped_column(Float, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    produto: Mapped["ProdutoModel"] = relationship("ProdutoModel")
    pedido = relationship("PedidoModel", back_populates="itens_pedido")
