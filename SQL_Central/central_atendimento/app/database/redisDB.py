import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        username=REDIS_USERNAME,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

    redis_client.ping()
    print("✅ Conectado ao Redis com sucesso!")

except Exception as e:
    print(f"❌ Erro ao conectar no Redis: {e}")
