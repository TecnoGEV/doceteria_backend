"""
Módulo que define o modelo ClienteModel para a doceteria.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import (
    Base,  # Certifique-se de que 'Base' está definido em config_model.py
)

if TYPE_CHECKING:
    from src.models.pedido_model import PedidoModel

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

    pedidos: Mapped[list[PedidoModel]] = relationship("PedidoModel", back_populates="cliente", lazy="selectin")

    class Config:
        from_attributes = True


