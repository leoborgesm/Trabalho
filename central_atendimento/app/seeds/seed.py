import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.database import db  

clientes = [
    {"nome": "João Silva", "email": "joao@email.com", "saldo": 1000},
    {"nome": "Maria Souza", "email": "maria@email.com", "saldo": 1500},
]

def popular_banco():
    if db.clientes.count_documents({}) == 0:  # Evita duplicação
        db.clientes.insert_many(clientes)
        print("Clientes inseridos no banco!")
    else:
        print("Clientes já existem no banco!")

if __name__ == "__main__":
    popular_banco()
