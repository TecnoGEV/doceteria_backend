"""
# -------------------------------
# Pivot Table: Receita Ingrediente
# -------------------------------
"""
from sqlalchemy import Column, ForeignKey, Integer, Table

from config.config_model import Base

receita_ingrediente_table = Table(
    "receita_ingrediente",
    Base.metadata,
    Column("receita_id", Integer, ForeignKey("receitas.id"), primary_key=True),
    Column(
        "ingrediente_id",
        Integer,
        ForeignKey("ingredientes.id"),
        primary_key=True,
    ),
)
