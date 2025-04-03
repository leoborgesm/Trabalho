from app.routes.analytics import router as analytics_router
from app.routes.cartoes import router as cartoes_router  # Se houver esse módulo

__all__ = ["analytics_router", "cartoes_router"]  # Inclua os routers necessários
