from fastapi import FastAPI, HTTPException
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from pydantic import BaseModel
from typing import List
import redis
import json

# Conectar ao MongoDB
uri = input("Digite sua URI aqui: ")
client = MongoClient(uri)
db = client["central_atendimento"]
colecao_clientes = db["clientes"]

# Criar índices eficientes
colecao_clientes.create_index([("cliente_id", ASCENDING), ("cartoes.cartao_id", ASCENDING)])  
colecao_clientes.create_index([("cliente_id", ASCENDING)])  

# Conectar ao Redis (usando seu endpoint na nuvem)
redis_client = redis.Redis(
    host="redis-14080.c308.sa-east-1-1.ec2.redns.redis-cloud.com",
    port=14080,
    decode_responses=True
)

# Inicializar o FastAPI
app = FastAPI()

# Modelos Pydantic para validação de dados
class Cartao(BaseModel):
    cartao_id: str
    numero_mascarado: str
    bandeira: str
    status: str
    motivo_bloqueio: str = None
    data_bloqueio: datetime = None
    limite_total: float
    limite_utilizado: float
    limite_disponivel: float

class BloqueioRequest(BaseModel):
    cliente_id: str
    cartao_id: str
    motivo: str

class LimiteResponse(BaseModel):
    cartao_id: str
    limite_total: float
    limite_utilizado: float
    limite_disponivel: float

@app.post("/bloquear_cartao")
async def bloquear_cartao(request: BloqueioRequest):
    cliente = colecao_clientes.find_one({"cliente_id": request.cliente_id})
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == request.cartao_id), None)
    
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")
    
    if cartao["status"] == "ativo":
        cartao["status"] = "bloqueado"
        cartao["motivo_bloqueio"] = request.motivo
        cartao["data_bloqueio"] = datetime.utcnow()

        operacao_bloqueio = {
            "tipo": "bloqueio",
            "cartao_id": request.cartao_id,
            "data": datetime.utcnow(),
            "motivo": request.motivo,
            "canal": "API"
        }
        cliente["historico_operacoes"].append(operacao_bloqueio)
        
        colecao_clientes.update_one(
            {"cliente_id": request.cliente_id},
            {"$set": {"cartoes": cliente["cartoes"], "historico_operacoes": cliente["historico_operacoes"]}}
        )

        # 🔴 REMOVER CACHE DO LIMITE PARA GARANTIR QUE OS DADOS ESTÃO ATUALIZADOS 🔴
        cache_key = f"limite:{request.cliente_id}:{request.cartao_id}"
        redis_client.delete(cache_key)

        return {"message": f"Cartão {request.cartao_id} bloqueado com sucesso!"}
    else:
        raise HTTPException(status_code=400, detail=f"Cartão {request.cartao_id} já está bloqueado.")

@app.get("/consultar_limite/{cliente_id}/{cartao_id}", response_model=LimiteResponse)
async def consultar_limite(cliente_id: str, cartao_id: str):
    cache_key = f"limite:{cliente_id}:{cartao_id}"

    # 🟢 1️⃣ Primeiro, tenta pegar o cache no Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # 🟢 2️⃣ Caso não tenha cache, busca no MongoDB
    cliente = colecao_clientes.find_one({"cliente_id": cliente_id})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == cartao_id), None)
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")

    # 🟢 3️⃣ Registrar operação e salvar no MongoDB
    operacao_consulta = {
        "tipo": "consulta_limite",
        "cartao_id": cartao_id,
        "data": datetime.utcnow(),
        "limite_disponivel": cartao["limite_disponivel"],
        "canal": "API"
    }
    cliente["historico_operacoes"].append(operacao_consulta)
    
    colecao_clientes.update_one(
        {"cliente_id": cliente_id},
        {"$set": {"historico_operacoes": cliente["historico_operacoes"]}}
    )

    # 🟢 4️⃣ Salvar no cache Redis por 30 segundos
    limite_info = {
        "cartao_id": cartao["cartao_id"],
        "limite_total": cartao["limite_total"],
        "limite_utilizado": cartao["limite_utilizado"],
        "limite_disponivel": cartao["limite_disponivel"]
    }
    
    redis_client.setex(cache_key, 30, json.dumps(limite_info))

    return limite_info
