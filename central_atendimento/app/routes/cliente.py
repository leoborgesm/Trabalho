from fastapi import APIRouter
from app.database import db  # Importando o banco de dados

router = APIRouter()

@router.get("/clientes")
async def listar_clientes():
    """Retorna todos os clientes cadastrados no MongoDB."""
    clientes = list(db.clientes.find({}, {"_id": 0}))  # Exclui o _id para simplificar
    return {"clientes": clientes}

