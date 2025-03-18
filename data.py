from pymongo.mongo_client import MongoClient
from datetime import datetime

uri = input("Para estabelecer conexao, escreva a URL do mongoDB aqui: ")

# Criar um novo cliente e conectar ao servidor
client = MongoClient(uri)

# Enviar um ping para confirmar a conexão bem-sucedida
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Erro de conexão:", e)

db = client["central_atendimento"]
colecao_clientes = db["clientes"]

# Documento de dados do cliente
dados_cliente = {
    "cliente_id": "12345",
    "nome": "João Silva",
    "email": "joao.silva@email.com",
    "telefone": "11987654321",
    "cartoes": [
        {
            "cartao_id": "cartao_001",
            "numero_mascarado": "**** **** **** 1234",
            "bandeira": "Visa",
            "status": "ativo",
            "limite_total": 5000,
            "limite_utilizado": 1000,
            "limite_disponivel": 4000
        }
    ],
    "historico_operacoes": [],
    "data_criacao": datetime.utcnow()  # Adicionando um campo de data
}

# Verificar se o cliente já existe na coleção (baseado no cliente_id)
cliente_existente = colecao_clientes.find_one({"cliente_id": dados_cliente["cliente_id"]})

if cliente_existente:
    # Atualizar o documento se já existir
    resultado = colecao_clientes.update_one(
        {"cliente_id": dados_cliente["cliente_id"]},
        {"$set": dados_cliente}
    )
    print(f"Documento atualizado com sucesso! {resultado.modified_count} documento(s) modificado(s).")
else:
    # Inserir o documento se não existir
    try:
        resultado = colecao_clientes.insert_one(dados_cliente)
        print(f"Documento inserido com ID: {resultado.inserted_id}")
    except Exception as e:
        print("Erro ao inserir o documento:", e)

# Buscar e exibir todos os clientes inseridos
print("\nClientes cadastrados:")
for cliente in colecao_clientes.find():
    print(cliente)
