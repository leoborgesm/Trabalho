from pydantic import BaseModel

class LimiteResponse(BaseModel):
    cartao_id: str
    limite_total: float
    limite_utilizado: float
    limite_disponivel: float
