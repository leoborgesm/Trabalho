from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Cartao(BaseModel):
    cartao_id: str
    numero_mascarado: str
    bandeira: str
    status: str
    motivo_bloqueio: Optional[str] = None
    data_bloqueio: Optional[datetime] = None
    limite_total: float
    limite_utilizado: float
    limite_disponivel: float


class BloqueioRequest(BaseModel):
    cartao_id: str
    motivo: Optional[str] = None

class LimiteResponse(BaseModel):
    cartao_id: str
    limite_disponivel: float
