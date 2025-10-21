"""SQLAlchemy ORM models for the doceteria backend."""

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


class Ingrediente(Base):
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
    receitas: Mapped[list["Receita"]] = relationship(
        "Receita", secondary=receita_ingrediente_table, back_populates="ingredientes"
    )


class Receita(Base):
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
    custo_total: Mapped[float] = mapped_column(Float)
    lucro_sugerido: Mapped[float] = mapped_column(Float)

    # Relação Many-to-Many com Ingredientes
    ingredientes: Mapped[list["Ingrediente"]] = relationship(
        "Ingrediente", secondary=receita_ingrediente_table, back_populates="receitas"
    )


class Categoria(Base):
    """
    Classe que representa uma categoria na doceteria.

    Attributes:
        id (int): O ID da categoria.
        categoria (str): O nome da categoria.
    """

    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoria: Mapped[str] = mapped_column(String(50))

    produtos: Mapped[list["Produto"]] = relationship(
        "Produto", back_populates="categoria"
    )


class Produto(Base):
    """
    Classe que representa um produto na doceteria.

    Attributes:
        id (int): O ID do produto.
        nome_produto (str): O nome do produto.
        receita_id (int): O ID da receita associada ao produto.
        receita (Receita): A receita associada ao produto.
        pedidos (List[Pedido]): A lista de pedidos relacionados ao produto.
    """

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_produto: Mapped[str] = mapped_column(String(150))
    data_validade: Mapped[str] = mapped_column(String(50))
    marca: Mapped[str] = mapped_column(String(50))
    codigo_barras: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    preco_unidade: Mapped[float] = mapped_column(Float)
    unidade: Mapped[str] = mapped_column(String(50))
    quantidade: Mapped[float] = mapped_column(Float)

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id"), nullable=True
    )
    categoria: Mapped["Categoria"] = relationship(
        "Categoria", back_populates="produtos"
    )
    # Uma receita pode gerar vários produtos (1-N)
    receita_id: Mapped[int] = mapped_column(ForeignKey("receitas.id"), nullable=True)
    receita: Mapped["Receita"] = relationship("Receita")

    pedidos: Mapped[list["Pedido"]] = relationship("Pedido", back_populates="produto")


class Venda(Base):
    """
    Classe que representa uma venda na doceteria.

    Attributes:
        id (int): O ID da venda.
        nome_cliente (str): O nome do cliente da venda.
        telefone (str): O telefone do cliente da venda.
        pedidos (List[Pedido]): A lista de pedidos relacionados à venda.
    """

    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_cliente: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[str] = mapped_column(String(20))

    pedidos: Mapped[list["Pedido"]] = relationship("Pedido", back_populates="venda")


class Pedido(Base):
    """
    Classe que representa um pedido na doceteria.

    Attributes:
        id (int): O ID do pedido.
        quantidade (float): A quantidade do pedido.
        preco (float): O preço do pedido.
        venda_id (int): O ID da venda relacionada ao pedido.
        produto_id (int): O ID do produto relacionado ao pedido.
        venda (Venda): A venda relacionada ao pedido.
        produto (Produto): O produto relacionado ao pedido.
    """

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantidade: Mapped[float] = mapped_column(Float)
    preco: Mapped[float] = mapped_column(Float)

    venda_id: Mapped[int] = mapped_column(ForeignKey("vendas.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))

    venda: Mapped["Venda"] = relationship("Venda", back_populates="pedidos")
    produto: Mapped["Produto"] = relationship("Produto", back_populates="pedidos")
