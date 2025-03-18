from pymongo import MongoClient
from datetime import datetime

# Conectar ao MongoDB
uri = input("URI AQUI: ")

client = MongoClient(uri)
db = client["central_atendimento"]
colecao_clientes = db["clientes"]

# Exemplo de dados de cliente para inserção/atualização
cliente = {
    "cliente_id": "",
    "nome": "",
    "email": "",
    "telefone": "",
    "cartoes": [
        {
            "cartao_id": "",
            "numero_mascarado": "",
            "bandeira": "",
            "status": "",
            "limite_total": ,
            "limite_utilizado": ,
            "limite_disponivel": 
        }
    ],
    "historico_operacoes": [],
    "data_criacao": datetime.utcnow()  # Adicionando um campo de data
}

# Verificar se o cliente já existe
cliente_existente = colecao_clientes.find_one({"cliente_id": cliente["cliente_id"]})

if cliente_existente:
    # Atualizar os dados do cliente existente
    colecao_clientes.update_one(
        {"cliente_id": cliente["cliente_id"]},
        {"$set": {
            "nome": cliente["nome"],
            "email": cliente["email"],
            "telefone": cliente["telefone"],
            "cartoes": cliente["cartoes"],  # Atualiza todos os cartões (pode ser ajustado conforme necessário)
            "data_criacao": cliente_existente.get("data_criacao", datetime.utcnow())  # Mantém a data original
        }}
    )
    print("Cliente atualizado com sucesso!")
else:
    # Inserir novo cliente
    colecao_clientes.insert_one(cliente)
    print("Cliente inserido com sucesso!")
