from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obter variáveis
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    print("✅ Conexão com Neo4j estabelecida com sucesso.")
except Exception as e:
    print(f"❌ Erro ao conectar com Neo4j: {e}")
    driver = None
