"""
# -------------------------------
# Item do Pedido Model
# -------------------------------
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.config_model import Base

if TYPE_CHECKING:
    from src.models.pedido_model import PedidoModel
    from src.models.produto_model import ProdutoModel

class ItemModel(Base):

    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    quantidade: Mapped[float] = mapped_column(Float, nullable=False)
    preco_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    produto: Mapped[ProdutoModel] = relationship("ProdutoModel", back_populates="itens_pedidos", lazy="selectin")
    pedido: Mapped[PedidoModel] = relationship("PedidoModel", back_populates="itens_pedido", lazy="selectin")
