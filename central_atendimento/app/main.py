from fastapi import FastAPI
from app.routes.analytics import router as analytics_router  # Certifique-se de importar corretamente
from app.routes.cartoes import router as cartoes_router  # Se houver outro router
from app.routes.cliente import router as cliente_router  # Importa o router de clientes


app = FastAPI()

app.include_router(analytics_router, prefix="/analytics")  # Certifique-se de incluir o router
app.include_router(cartoes_router, prefix="/cartoes")  # Se houver outro router
app.include_router(cliente_router, prefix="/clientes")  # Adiciona a rota de clientes

