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


# 📊 Analytics: status mais comuns entre todos os clientes
@router.get("/analytics/status-mais-comuns")
def status_mais_comuns():
    query = """
    MATCH (:Cliente)-[r:MUDOU_PARA]->(s:Status)
    RETURN s.tipo AS status, COUNT(r) AS vezes
    ORDER BY vezes DESC
    """
    with driver.session() as session:
        result = session.run(query)
        analise = [{"status": record["status"], "vezes": record["vezes"]} for record in result]
    
    if not analise:
        raise HTTPException(status_code=404, detail="Nenhum status encontrado")

    return {"analise": analise}


#Ranking para saber o cliente mais ativo 
@router.get("/analytics/clientes-mais-ativos")
def clientes_mais_ativos():
    query = """
    MATCH (c:Cliente)-[r:MUDOU_PARA]->()
    RETURN c.id AS cliente_id, COUNT(r) AS alteracoes
    ORDER BY alteracoes DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        ranking = [{"cliente_id": record["cliente_id"], "alteracoes": record["alteracoes"]} for record in result]

    if not ranking:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado")

    return {"ranking": ranking}


@router.get("/caminho-status")
def caminho_entre_status(inicio: str, fim: str):
    query = """
    MATCH (s1:Status {tipo: $inicio}), (s2:Status {tipo: $fim})
    MATCH p = shortestPath((s1)-[*..10]-(s2))
    RETURN [n IN nodes(p) | n.tipo] AS caminho
    """
    with driver.session() as session:
        result = session.run(query, inicio=inicio, fim=fim)
        caminho = [record["caminho"] for record in result]

    if not caminho:
        raise HTTPException(status_code=404, detail="Nenhum caminho encontrado entre os status")

    return {"caminho": caminho}



"""
ativo → suspenso → aguardando_verificacao → bloqueado

“Qual o menor caminho entre o status ativo e o status bloqueado que já foi percorrido no grafo?”

MATCH (s1:Status {tipo: "ativo"}), (s2:Status {tipo: "bloqueado"})
MATCH p = shortestPath((s1)-[*..10]-(s2))
RETURN [n IN nodes(p) | n.tipo] AS caminho

["ativo", "suspenso", "aguardando_verificacao", "bloqueado"]



"""

@router.get("/analytics/predicao-bloqueio-retorno")
def predicao_retorno_apos_bloqueio():
    query = """
    MATCH (c:Cliente)-[:MUDOU_PARA]->(s:Status {tipo: "bloqueado"})
    WITH COLLECT(DISTINCT c.id) AS bloqueados

    MATCH (c:Cliente)-[:MUDOU_PARA]->(s2:Status {tipo: "ativo"})
    WHERE c.id IN bloqueados
    WITH COUNT(DISTINCT c.id) AS voltaram_ativo, SIZE(bloqueados) AS total_bloqueados

    RETURN voltaram_ativo, total_bloqueados,
           ROUND(toFloat(voltaram_ativo) / total_bloqueados * 100, 2) AS porcentagem
    """
    with driver.session() as session:
        result = session.run(query)
        dados = result.single()
    
    if not dados:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado.")

    return {
        "total_bloqueados": dados["total_bloqueados"],
        "voltaram_ativo": dados["voltaram_ativo"],
        "porcentagem": dados["porcentagem"]
    }


'''
// Total de clientes que chegaram a ser bloqueados
MATCH (c:Cliente)-[:MUDOU_PARA]->(s:Status {tipo: "bloqueado"})
WITH COLLECT(DISTINCT c.id) AS bloqueados

// Destes, quantos também voltaram a ativo
MATCH (c:Cliente)-[:MUDOU_PARA]->(s2:Status {tipo: "ativo"})
WHERE c.id IN bloqueados
WITH COUNT(DISTINCT c.id) AS voltaram_ativo, SIZE(bloqueados) AS total_bloqueados

RETURN voltaram_ativo, total_bloqueados,
       ROUND(toFloat(voltaram_ativo) / total_bloqueados * 100, 2) AS porcentagem

Esperado? 
{
  "voltaram_ativo": 12,
  "total_bloqueados": 20,
  "porcentagem": 60.0
}
              
'''
