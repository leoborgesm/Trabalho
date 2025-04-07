from datetime import datetime
from app.database.neo4jDB import driver

def registrar_historico_status(cliente_id, novo_status):
    if not driver:
        print("❌ Driver do Neo4j não disponível.")
        return

    try:
        with driver.session() as session:
            session.run("""
                MERGE (c:Cliente {id: $cliente_id})
                MERGE (s:Status {tipo: $status})
                CREATE (c)-[:MUDOU_PARA {data: $data_hora}]->(s)
            """, cliente_id=cliente_id, status=novo_status, data_hora=datetime.now().isoformat())

            print(f"✅ Histórico de alteração salvo no Neo4j para cliente {cliente_id} → {novo_status}")
    except Exception as e:
        print("❌ Erro ao registrar histórico no Neo4j:", e)
