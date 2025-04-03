from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Obtendo a URI do MongoDB
MONGO_URI = os.getenv("MONGO_URI")

# Criando conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database()  # Obtém o banco automaticamente da URI

# Coleções utilizadas
colecao_clientes = db["clientes"]
