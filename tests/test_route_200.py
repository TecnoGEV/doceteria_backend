from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_categoria_index():
    response = client.get("/categorias")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cliente_index():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_pedido_index():
    response = client.get("/pedidos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_produto_index():
    response = client.get("/produtos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_receita_index():
    response = client.get("/receitas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_venda_index():
    response = client.get("/vendas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
