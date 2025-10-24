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
