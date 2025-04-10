from app.database.mongoDB import client
from app.database.redisDB import redis_client
from app.utils.historico import registrar_historico_status

# Versão para o terminal
def alterar_status_cartao(cliente_id, novo_status):
    db = client["central_atendimento"]
    clientes = db["clientes"]

    doc = clientes.find_one({"cliente_id": cliente_id})

    if not doc:
        print(f"❌ Cliente com ID {cliente_id} não encontrado.")
        return

    try:
        resultado = clientes.update_one(
            {"cliente_id": cliente_id},
            {"$set": {"cartoes.0.status": novo_status}}
        )

        if resultado.modified_count > 0:
            print(f"✅ Cartão atualizado para: {novo_status}")
        else:
            print("ℹ️ Nenhuma modificação foi feita (status já pode estar igual).")

    except Exception as e:
        print("❌ Erro ao atualizar o status do cartão.")
        print(f"Detalhes: {e}")


# NOVA FUNÇÃO para API
def alterar_status_cartao_api(cliente_id, novo_status):
    db = client["central_atendimento"]
    clientes = db["clientes"]

    doc = clientes.find_one({"cliente_id": cliente_id})
    if not doc:
        return {"erro": f"Cliente com ID {cliente_id} não encontrado."}

    try:
        resultado = clientes.update_one(
            {"cliente_id": cliente_id},
            {"$set": {"cartoes.0.status": novo_status}}
        )

        # Atualiza no Redis
        bit_valor = 1 if novo_status.lower() == "ativo" else 0
        redis_client.setbit("status_cartoes", int(cliente_id), bit_valor)

        # Salva no Neo4j
        registrar_historico_status(cliente_id, novo_status)

        if resultado.modified_count > 0:
            return {"mensagem": f"Cartão atualizado para: {novo_status}"}
        else:
            return {"mensagem": "Nenhuma modificação foi feita. O status já pode estar igual."}

    except Exception as e:
        return {
            "erro": "Erro ao atualizar o status do cartão.",
            "detalhes": str(e)
        }
