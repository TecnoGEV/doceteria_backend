from pydantic import BaseModel


class ItemScherma(BaseModel):
    produto_id: int
    pedido_id: int
    quantidade: float
    preco_unitario: float

    class ConfigDict:
        from_attributes = True
