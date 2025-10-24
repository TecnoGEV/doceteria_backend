from pydantic import BaseModel


class CategoriaScherma(BaseModel):
    """
    _summary_

    Args:
       Scherma BaseModel (_type_): _description_
    """
    categoria: str

    class ConfigDict:
        from_attributes = True
