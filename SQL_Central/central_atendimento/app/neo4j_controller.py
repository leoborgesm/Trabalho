from fastapi import APIRouter, HTTPException
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Conexão com o Neo4j
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(user, password))

@router.get("/historico/{cliente_id}")
def get_historico(cliente_id: str):
    query = """
    MATCH (c:Cliente {id: $cliente_id})-[r:MUDOU_PARA]->(s:Status)
    RETURN s.tipo AS status, r.data AS data
    ORDER BY r.data DESC
    """
    with driver.session() as session:
        result = session.run(query, cliente_id=cliente_id)
        historico = [{"status": record["status"], "data": record["data"]} for record in result]

    if not historico:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")

    return {"cliente_id": cliente_id, "historico": historico}
