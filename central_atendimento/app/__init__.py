from fastapi import FastAPI

# Importar as rotas
from app.routes.cartoes import router as cartoes_router
from app.routes.cliente import router as cliente_router


# Criar a instância do FastAPI
app = FastAPI(title="Central de Atendimento", version="1.0")

# Registrar as rotas na aplicação
app.include_router(cartoes_router, prefix="/cartao", tags=["Cartão"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])

# Mensagem de boas-vindas
@app.get("/")
async def root():
    return {"message": "Bem-vindo à Central de Atendimento!"}
