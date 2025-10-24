from pydantic import BaseModel
from .pedido_scherma import PedidoScherma

class VendaScherma(BaseModel):
    pedido: PedidoScherma
    forma_pagamento: str
    status_venda: str

    class ConfigDictDict:
        from_attributes = True
