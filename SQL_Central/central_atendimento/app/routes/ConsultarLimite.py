from app.database.mongoDB import client
from app.database.redisDB import redis_client
from redis.exceptions import ResponseError
# Continua funcionando pro menu de terminal
def consultar_limite(cliente_id):
    db = client["central_atendimento"]
    clientes = db["clientes"]

    doc = clientes.find_one({"cliente_id": cliente_id})

    if not doc:
        print(f"❌ Cliente com ID {cliente_id} não encontrado.")
        return

    try:
        cartao = doc["cartoes"][0]

        limite_total = cartao.get("limite_total", 0)
        limite_utilizado = cartao.get("limite_utilizado", 0)
        limite_disponivel = cartao.get("limite_disponivel", 0)

        print("\n💳 Informações de Limite:")
        print(f"Limite total:       R$ {limite_total:.2f}")
        print(f"Limite utilizado:   R$ {limite_utilizado:.2f}")
        print(f"Limite disponível:  R$ {limite_disponivel:.2f}")

    except (KeyError, IndexError) as e:
        print("❌ Erro ao acessar informações do cartão.")
        print(f"Detalhes: {e}")






# NOVA FUNÇÃO: ideal para FastAPI
BLOOM_FILTER_KEY = "clientes_bloom"

def consultar_limite_api(cliente_id):
    try:
        # 1. Verifica no Bloom Filter se o cliente possivelmente existe
        existe = redis_client.execute_command("BF.EXISTS", BLOOM_FILTER_KEY, cliente_id)

        if existe == 0:
            return {"erro": f"Cliente {cliente_id} provavelmente não existe."}

        # 2. Tenta pegar do Redis Cache
        cache_key = f"limite:{cliente_id}"
        dados_em_cache = redis_client.get(cache_key)

        if dados_em_cache:
            return eval(dados_em_cache)  # cuidado: apenas para testes, evite eval em produção

        # 3. Busca no MongoDB
        db = client["central_atendimento"]
        clientes = db["clientes"]
        doc = clientes.find_one({"cliente_id": cliente_id})

        if not doc:
            return {"erro": f"Cliente {cliente_id} não encontrado no banco."}

        cartao = doc["cartoes"][0]
        resposta = {
            "cliente_id": cliente_id,
            "limite_total": cartao.get("limite_total", 0),
            "limite_utilizado": cartao.get("limite_utilizado", 0),
            "limite_disponivel": cartao.get("limite_disponivel", 0)
        }

        # 4. Adiciona no cache Redis e no Bloom Filter
        redis_client.set(cache_key, str(resposta), ex=300)  # TTL de 5 minutos
        try:
            redis_client.execute_command("BF.ADD", BLOOM_FILTER_KEY, cliente_id)
        except ResponseError:
            # Se o filtro ainda não existir, cria com parâmetros default
            redis_client.execute_command("BF.RESERVE", BLOOM_FILTER_KEY, 0.01, 1000)
            redis_client.execute_command("BF.ADD", BLOOM_FILTER_KEY, cliente_id)

        return resposta

    except Exception as e:
        return {"erro": "Erro interno ao consultar limite", "detalhes": str(e)}