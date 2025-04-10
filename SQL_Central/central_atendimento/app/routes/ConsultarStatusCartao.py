from app.database.mongoDB import client

# Versão para o terminal
def consultar_status_cartao(cliente_id):
    db = client["central_atendimento"]
    clientes = db["clientes"]

    doc = clientes.find_one({"cliente_id": cliente_id})

    if not doc:
        print(f"❌ Cliente com ID {cliente_id} não encontrado.")
        return

    try:
        cartao = doc["cartoes"][0]
        status = cartao.get("status", "Indefinido")

        print("\n🛡️ Status do Cartão:")
        print(f"Status atual: {status}")

    except (KeyError, IndexError) as e:
        print("❌ Erro ao acessar o status do cartão.")
        print(f"Detalhes: {e}")


# NOVA função para uso com FastAPI
def consultar_status_cartao_api(cliente_id):
    db = client["central_atendimento"]
    clientes = db["clientes"]

    doc = clientes.find_one({"cliente_id": cliente_id})

    if not doc:
        return {"erro": f"Cliente com ID {cliente_id} não encontrado."}

    try:
        cartao = doc["cartoes"][0]
        status = cartao.get("status", "Indefinido")

        return {
            "cliente_id": cliente_id,
            "status_cartao": status
        }

    except (KeyError, IndexError) as e:
        return {
            "erro": "Erro ao acessar o status do cartão.",
            "detalhes": str(e)
        }
