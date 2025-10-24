from pydantic import BaseModel
from .item_scherma import ItemScherma


class PedidoScherma(BaseModel):
    cliente_id: int
    itens_pedido: list[ItemScherma]
    preco_total: float

    class ConfigDictDict:
        from_attributes = True
