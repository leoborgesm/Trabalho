from fastapi import APIRouter, HTTPException
from app.database.mongo import colecao_clientes
from app.database.redis import set_cartao_bloqueado, is_cartao_bloqueado, registrar_acesso_limite , total_acessos_limite
from app.models.cartoes import BloqueioRequest, LimiteResponse

router = APIRouter()

@router.post("/bloquear_cartao")
async def bloquear_cartao(request: BloqueioRequest):
    cliente = colecao_clientes.find_one({"cliente_id": request.cliente_id})
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == request.cartao_id), None)
    
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")

    if cartao["status"] == "ativo":
        # Atualizar MongoDB
        cartao["status"] = "bloqueado"
        cartao["motivo_bloqueio"] = request.motivo
        colecao_clientes.update_one(
            {"cliente_id": request.cliente_id},
            {"$set": {"cartoes": cliente["cartoes"]}}
        )
        
        # Atualizar Redis (Bitmap)
        set_cartao_bloqueado(request.cartao_id, True)

        return {"message": f"Cartão {request.cartao_id} bloqueado com sucesso!"}
    
    raise HTTPException(status_code=400, detail=f"Cartão {request.cartao_id} já está bloqueado.")

@router.get("/consultar_limite/{cliente_id}/{cartao_id}", response_model=LimiteResponse)
async def consultar_limite(cliente_id: str, cartao_id: str):
    cliente = colecao_clientes.find_one({"cliente_id": cliente_id})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    cartao = next((c for c in cliente["cartoes"] if c["cartao_id"] == cartao_id), None)
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado.")

    # Contar acesso ao limite (HyperLogLog)
    registrar_acesso_limite(cartao_id)

    return LimiteResponse(
        cartao_id=cartao["cartao_id"],
        limite_total=cartao["limite_total"],
        limite_utilizado=cartao["limite_utilizado"],
        limite_disponivel=cartao["limite_disponivel"]
    )

@router.get("/total_acessos_limite")
async def total_acessos():
    total = total_acessos_limite()
    return {"total_acessos_unicos": total}
