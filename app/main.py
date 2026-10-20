from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.assistidos.router import router as assistidos_router
from app.modules.voluntarios.router import router as voluntarios_router
from app.modules.aulas.router import router as aulas_router
from app.modules.chamadas.router import router as chamadas_router

# Inicialização da aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração do CORS (para o Front conseguir consumir a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Depois: especifique as URLs do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas dos módulos
app.include_router(assistidos_router, prefix=settings.API_V1_STR)
app.include_router(voluntarios_router, prefix=settings.API_V1_STR)
app.include_router(aulas_router, prefix=settings.API_V1_STR)
app.include_router(chamadas_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Healthcheck"])
async def root():
    """Endpoint básico para verificar se a API está online"""
    return{
        "status": "online",
        "projeto": settings.PROJECT_NAME,
        "versao": settings.VERSION,
        "docs": "/docs"
    }