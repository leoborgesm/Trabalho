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
  "nome": "Leonardo Morais",
  "cpf": "123.456.789-00",
  "telefone": "+55 31 98765-4321",
  "email": "leonardo@email.com",
  "cartoes": [
    {
      "cartao_id": "987654321",
      "numero_mascarado": "**** **** **** 4321",
      "bandeira": "Visa",
      "status": "bloqueado",
      "motivo_bloqueio": "roubo",
      "data_bloqueio": datetime.utcnow(),
      "limite_total": 5000.00,
      "limite_utilizado": 3200.00,
      "limite_disponivel": 1800.00
    },
    {
      "cartao_id": "123987654",
      "numero_mascarado": "**** **** **** 8765",
      "bandeira": "Mastercard",
      "status": "ativo",
      "limite_total": 7000.00,
      "limite_utilizado": 2500.00,
      "limite_disponivel": 4500.00
    }
  ],
  "historico_operacoes": [
    {
      "tipo": "bloqueio",
      "cartao_id": "987654321",
      "data": datetime.utcnow(),
      "motivo": "roubo",
      "canal": "App Mobile"
    },
    {
      "tipo": "consulta_limite",
      "cartao_id": "987654321",
      "data": datetime.utcnow(),
      "limite_disponivel": 1800.00,
      "canal": "App Mobile"
    }
  ]
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
