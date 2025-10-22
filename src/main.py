from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine
from src.models import Base
from src.routers.categorias_router import categoria_router
from src.routers.cliente_router import cliente_router
from src.routers.pedido_router import pedido_router
from src.routers.produto_router import produto_router
from src.routers.receita_router import receita_router
from src.routers.venda_router import venda_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente_router)
app.include_router(pedido_router)
app.include_router(produto_router)
app.include_router(receita_router)
app.include_router(venda_router)
app.include_router(categoria_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
