from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel

# Conectar ao MongoDB
uri = input("Para estabelecer conexao, escreva a URL do mongoDB aqui: ")
client = MongoClient(uri)
db = client["central_atendimento"]
colecao_clientes = db["clientes"]

app = FastAPI()

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
    # Buscar o cliente no banco de dados
    cliente = colecao_clientes.find_one({"cliente_id": request.cliente_id})
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    # Buscar o cartão do cliente
    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == request.cartao_id), None)
    
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")
    
    if cartao["status"] == "ativo":
        # Bloquear o cartão
        cartao["status"] = "bloqueado"
        cartao["motivo_bloqueio"] = request.motivo
        cartao["data_bloqueio"] = datetime.utcnow()

        # Registrar a operação no histórico
        operacao_bloqueio = {
            "tipo": "bloqueio",
            "cartao_id": request.cartao_id,
            "data": datetime.utcnow(),
            "motivo": request.motivo,
            "canal": "API"
        }
        cliente["historico_operacoes"].append(operacao_bloqueio)
        
        # Atualizar o cliente no banco de dados
        colecao_clientes.update_one(
            {"cliente_id": request.cliente_id},
            {"$set": {"cartoes": cliente["cartoes"], "historico_operacoes": cliente["historico_operacoes"]}}
        )
        return {"message": f"Cartão {request.cartao_id} bloqueado com sucesso!"}
    else:
        raise HTTPException(status_code=400, detail=f"Cartão {request.cartao_id} já está bloqueado.")

@app.get("/consultar_limite/{cliente_id}/{cartao_id}", response_model=LimiteResponse)
async def consultar_limite(cliente_id: str, cartao_id: str):
    # Buscar o cliente no banco de dados
    cliente = colecao_clientes.find_one({"cliente_id": cliente_id})
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    # Buscar o cartão do cliente
    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == cartao_id), None)
    
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")
    
    # Registrar a operação de consulta no histórico
    operacao_consulta = {
        "tipo": "consulta_limite",
        "cartao_id": cartao_id,
        "data": datetime.utcnow(),
        "limite_disponivel": cartao["limite_disponivel"],
        "canal": "API"
    }
    cliente["historico_operacoes"].append(operacao_consulta)
    
    # Atualizar o cliente no banco de dados
    colecao_clientes.update_one(
        {"cliente_id": cliente_id},
        {"$set": {"historico_operacoes": cliente["historico_operacoes"]}}
    )
    
    # Retornar a resposta com as informações do limite
    return LimiteResponse(
        cartao_id=cartao.cartao_id,
        limite_total=cartao.limite_total,
        limite_utilizado=cartao.limite_utilizado,
        limite_disponivel=cartao.limite_disponivel
    )
