import redis
import os
import hashlib

# Configuração do Redis
REDIS_HOST = "redis-14080.c308.sa-east-1-1.ec2.redns.redis-cloud.com"
REDIS_PORT = 14080
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "sua_senha_aqui")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# Função para gerar um índice único baseado no ID do cartão
def get_cartao_index(cartao_id: str) -> int:
    return int(hashlib.md5(cartao_id.encode()).hexdigest(), 16) % 1000000  # Índice entre 0 e 999999

# Função para definir status do cartão no Bitmap
def set_cartao_bloqueado(cartao_id: str, bloqueado: bool):
    bit = 1 if bloqueado else 0
    index = get_cartao_index(cartao_id)
    redis_client.setbit("cartoes_bloqueados", index, bit)

# Função para verificar se um cartão está bloqueado
def is_cartao_bloqueado(cartao_id: str) -> bool:
    index = get_cartao_index(cartao_id)
    return redis_client.getbit("cartoes_bloqueados", index) == 1

# Função para adicionar contagem de acesso único no HyperLogLog
def registrar_acesso_limite(cartao_id: str):
    redis_client.pfadd("acessos_limite", cartao_id)

# Função para obter contagem total de acessos únicos
def total_acessos_limite() -> int:
    return redis_client.pfcount("acessos_limite")
