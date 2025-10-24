from pydantic import BaseModel


class ClienteScherma(BaseModel):
    nome: str
    telefone: str
    endereco: str

    class ConfigDict:
        from_attributes = True
