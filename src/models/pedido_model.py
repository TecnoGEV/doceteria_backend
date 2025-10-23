"""
# -------------------------------
# Pedido
# -------------------------------
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base

if TYPE_CHECKING:
    from src.models.cliente_model import ClienteModel
    from src.models.item_model import ItemModel
    from src.models.venda_model import VendaModel


class PedidoModel(Base):

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_total: Mapped[float] = mapped_column(Float, nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

    cliente: Mapped[ClienteModel] = relationship(
        "ClienteModel", back_populates="pedidos", lazy="selectin"
    )

    itens_pedido: Mapped[list[ItemModel]] = relationship(
        "ItemModel", back_populates="pedido", cascade="all, delete", lazy="selectin"
    )

    # 🔗 Relacionamento 1:1 com Venda
    venda: Mapped[VendaModel] = relationship(
        "VendaModel",
        back_populates="pedido",
        uselist=False,  # garante 1:1
        cascade="all, delete-orphan",
        lazy="selectin",
    )
