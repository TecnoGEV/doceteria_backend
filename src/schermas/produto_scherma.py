from pydantic import BaseModel


class ProdutoScherma(BaseModel):
    """
    _summary_

    Args:
       Scherma BaseModel (_type_): _description_
    """

    nome_produto: str
    data_validade: str
    marca: str
    codigo_barras: str
    preco_unidade: float
    unidade: str
    quantidade: float
    categoria_id: int

    class ConfigDict:
        from_attributes = True

