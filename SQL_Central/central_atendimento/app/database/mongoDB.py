from pymongo import MongoClient
import pprint
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))

import central_atendimento


mongo_uri = os.getenv("MONGO_DB_URI")

client = MongoClient(mongo_uri)

try:
    client.admin.command('ping')
    print('Conexão Estabelecida com sucesso com o MongoDB')
except Exception as e:
    print('Erro ao tentar se conectar com MongoDB')
