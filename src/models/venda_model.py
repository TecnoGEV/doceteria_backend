"""
# -------------------------------
# Venda model
# -------------------------------
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base

if TYPE_CHECKING:
    from src.models.pedido_model import PedidoModel


class VendaModel(Base):

    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), unique=True)
    forma_pagamento: Mapped[str] = mapped_column(String(50), nullable=False)
    status_venda: Mapped[str] = mapped_column(String(50), nullable=False)

    pedido: Mapped[PedidoModel] = relationship(
        "PedidoModel", back_populates="venda", lazy="selectin"
    )
