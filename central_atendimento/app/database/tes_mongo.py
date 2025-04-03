from pymongo import MongoClient
import os
from dotenv import load_dotenv


# Carregar variáveis do .env
load_dotenv()

# Criando conexão manualmente com parâmetros extras
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

try:
    db = client["central_atendimento"]
    print("Conexão bem-sucedida! 🎉")
    print("Coleções disponíveis:", db.list_collection_names())
except Exception as e:
    print("Erro ao conectar:", e)
