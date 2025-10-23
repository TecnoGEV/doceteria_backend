"""
# -------------------------------
# Receita Model
# -------------------------------
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base
from src.models.pivot_ingrediente_receita import receita_ingrediente_table

if TYPE_CHECKING:
    from src.models.ingrediente_model import IngredienteModel


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
    ingredientes: Mapped[list[IngredienteModel]] = relationship(
        "IngredienteModel",
        secondary=receita_ingrediente_table,
        back_populates="receitas",
        lazy="selectin",
    )
