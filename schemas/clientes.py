from model import *
from pydantic import BaseModel

class ClientesSchema(BaseModel):
    nome: str
    email: str
    celular: str
    cidade: str

class FindClienteSchema(BaseModel):
    id: int

def get_cliente(cliente: Clientes):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "celular": cliente.celular,
        "cidade": cliente.cidade
    }