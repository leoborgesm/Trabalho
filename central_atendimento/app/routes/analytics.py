from fastapi import APIRouter
from app.database import redis_client  # Certifique-se de que esse import está correto

router = APIRouter()  # TEM que estar com esse nome para ser importado corretamente

@router.get("/top-cartoes")
async def top_cartoes():
    """Retorna os cartões mais consultados recentemente (usando HyperLogLog)."""
    cartoes_mais_consultados = redis_client.keys("consulta_cartao:*")
    return {"cartoes_populares": cartoes_mais_consultados}

@router.get("/historico-operacoes/{cliente_id}")
async def historico_operacoes(cliente_id: str):
    """Recupera o histórico de operações armazenado em Redis."""
    historico = redis_client.lrange(f"historico:{cliente_id}", 0, -1)
    return {"cliente_id": cliente_id, "historico": historico}
