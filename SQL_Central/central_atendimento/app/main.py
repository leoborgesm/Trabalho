from fastapi import FastAPI
from app.routes.ConsultarLimite import consultar_limite_api
from app.routes.ConsultarStatusCartao import consultar_status_cartao_api
from app.routes.AlterarStatusCartao import alterar_status_cartao_api
from app.neo4j_controller import router as historico_router

app = FastAPI(title="Central de Atendimento", version="1.0")

@app.get("/")
def home():
    return {"mensagem": "🚀 API Central de Atendimento no ar!"}

@app.get("/limite/{cliente_id}")
def rota_consultar_limite(cliente_id: str):
    return consultar_limite_api(cliente_id)

@app.get("/status/{cliente_id}")
def rota_consultar_status(cliente_id: str):
    return consultar_status_cartao_api(cliente_id)

@app.put("/status/{cliente_id}")
def rota_alterar_status(cliente_id: str, novo_status: str):
    return alterar_status_cartao_api(cliente_id, novo_status)

# Neo4j - rotas de histórico, análises e predições
app.include_router(historico_router, prefix="/neo4j", tags=["Análises com Grafos (Neo4j)"])
