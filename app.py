from flask import Flask, redirect, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from model import *
from schemas import *
from sqlalchemy.orm.session import close_all_sessions

from sqlalchemy.exc import IntegrityError


info = Info(title="Minha API", description="Minha documentação de API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

redirect_tag = Tag(name="Redirect", description="Rota utilizada no redirecionamento para a documentação")
clientes_tag = Tag(name="Clientes", description="todas as rotas da tabela de clientes")

@app.get("/", tags=[redirect_tag])
def hello_world():
    return redirect("/openapi")

@app.get("/clientes", tags=[clientes_tag])
def getClientes():
    """Lê todos os clientes
    """
    session = Session()
    clientes = session.query(Clientes).all()
    close_all_sessions()
    return jsonify({"clientes": [get_cliente(cliente) for cliente in clientes]})

@app.post("/clientes", tags=[clientes_tag])
def postClientes(form: ClientesSchema):
    """cria um cliente na tabela
    """
    cliente = Clientes(
        nome=form.nome,
        email=form.email,
        celular=form.celular,
        cidade=form.cidade
    )

    try:
        session = Session()
        session.add(cliente)
        session.commit()
        close_all_sessions()
        return "cliente cadastrado com sucesso!", 201
    
    except IntegrityError as e:
        session.rollback()
        error = e.args
        return {"message": error}, 400
    
@app.delete("/clientes", tags=[clientes_tag])
def deleteCliente(form: FindClienteSchema):
    """deleta um cliente
    """
    session = Session()
    excluido = session.query(Clientes).filter(Clientes.id == form.id).delete()
    
    if excluido:
        session.commit()
        close_all_sessions()
        return "Cliente excluido com sucesso!"
    
    else:
        return "Cliente não encontrado no banco"






