"""
# -------------------------------
# Ingrediente Model
# -------------------------------
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base
from src.models.pivot_ingrediente_receita import receita_ingrediente_table

if TYPE_CHECKING:
    from src.models.receita_model import ReceitaModel


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
    receitas: Mapped[list[ReceitaModel]] = relationship(
        "ReceitaModel",
        secondary=receita_ingrediente_table,
        back_populates="ingredientes",
        lazy="selectin"
    )


