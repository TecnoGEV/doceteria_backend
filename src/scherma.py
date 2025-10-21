"""Schemas for the doceteria backend."""

from pydantic import BaseModel


class ReceitaScherma(BaseModel):
    """_summary_

    Args:
       Scherma BaseModel (_type_): _description_
    """

    nome_receita: str
    porcao_rendimento: str
    ingrediente: list[str]
    quantidade: list[float]
    modo_preparo: str
    margem_lucro: float
    preco_sugerido: float
    preco_venda: float
    custo_porcao: float
    custo_total: float
    lucro_sugerido: float

    class Config:
        """_summary_"""

        from_attributes = True


class CategoriaScherma(BaseModel):
    """
    _summary_

    Args:
       Scherma BaseModel (_type_): _description_
    """

    categoria: str

    class Config:
        from_attributes = True


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
    categoria: CategoriaScherma

    class Config:
        from_attributes = True


class VendaScherma(BaseModel):
    nome_cliente: str
    telefone: str
    item: list[ProdutoScherma]

    class Config:
        from_attributes = True


class PedidoScherma(BaseModel):
    venda: VendaScherma
    produto: ProdutoScherma
    quantidade: float
    preco: float

    class Config:
        from_attributes = True
