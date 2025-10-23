"""
#
# -------------------------------
# Produto Model
# -------------------------------
#
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base

if TYPE_CHECKING:
    from src.models.categoria_model import CategoriaModel
    from src.models.item_model import ItemModel

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


    categoria: Mapped[CategoriaModel] = relationship(
        "CategoriaModel", back_populates="produtos", lazy="selectin"
    )

    itens_pedidos: Mapped[list[ItemModel]] = relationship(
        "ItemModel", back_populates="produto", lazy="selectin"
    )

