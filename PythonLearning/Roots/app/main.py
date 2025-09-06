from fastapi import FastAPI
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Roots Store API", version="0.1.0")

    # Routers
    from .routers.health import router as health_router
    from .routers.catalog import router as catalog_router
    from .routers.orders import router as orders_router
    from .routers.whatsapp import router as whatsapp_router
    from .routers.auth import router as auth_router

    app.include_router(health_router, prefix="/health", tags=["health"]) 
    app.include_router(catalog_router, prefix="/catalog", tags=["catalog"]) 
    app.include_router(orders_router, prefix="/orders", tags=["orders"]) 
    app.include_router(whatsapp_router, prefix="/whatsapp", tags=["whatsapp"])
    app.include_router(auth_router, prefix="/auth", tags=["auth"]) 

    return app


app = create_app()


