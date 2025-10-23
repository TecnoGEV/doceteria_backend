"""
#
# ---------------------------------
# Categoria Model
# ---------------------------------
#
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base

if TYPE_CHECKING:
    from src.models.produto_model import ProdutoModel


class CategoriaModel(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)

    produtos: Mapped[list[ProdutoModel]] = relationship(
        "ProdutoModel",
        back_populates="categoria",
        cascade="all, delete",
        lazy="selectin",
    )
