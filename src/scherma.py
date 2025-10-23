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

    class ConfigDict:
        """_summary_"""

        from_attributes = True


class CategoriaScherma(BaseModel):
    """
    _summary_

    Args:
       Scherma BaseModel (_type_): _description_
    """

    categoria: str

    class ConfigDict:
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
    categoria_id: int

    class ConfigDict:
        from_attributes = True


class ClienteScherma(BaseModel):
    nome: str
    telefone: str
    endereco: str

    class ConfigDict:
        from_attributes = True


class ItemScherma(BaseModel):
    produto_id: int
    pedido_id: int
    quantidade: float
    preco_unitario: float

    class ConfigDict:
        from_attributes = True


class PedidoScherma(BaseModel):
    cliente_id: int
    itens_pedido: list[ItemScherma]
    preco_total: float

    class ConfigDictDict:
        from_attributes = True


class VendaScherma(BaseModel):
    pedido: PedidoScherma
    forma_pagamento: str
    status_venda: str

    class ConfigDictDict:
        from_attributes = True
