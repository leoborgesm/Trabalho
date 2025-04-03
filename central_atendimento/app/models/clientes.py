from pydantic import BaseModel
from typing import List, Dict, Any
from .cartoes import Cartao

class Cliente(BaseModel):
    cliente_id: str
    nome: str
    email: str
    telefone: str
    cartoes: List[Cartao] = []
    historico_operacoes: List[Dict[str, Any]] = []
