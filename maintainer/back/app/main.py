from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import alerted_users

app = FastAPI(
    title="Maintainer Web Hook API",
    description="API for managing maintenance web hooks",
    version="1.0.0",
    docs_url="/docs" if settings.dev else None,
    redoc_url="/redoc" if settings.dev else None
)

# Ensure required directories exist
settings.ensure_directories()

# Configurar CORS según entorno
def setup_cors(app):
    if settings.dev:
        # En desarrollo: no aplicar ninguna política de CORS (permitir todo)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        # En producción: restringir a orígenes definidos en config.json
        cors_origins = getattr(settings, "cors", None)
        if not cors_origins or not isinstance(cors_origins, list):
            cors_origins = []
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

# Include routers
app.include_router(alerted_users.router)

@app.on_event("startup")
async def startup_event():
    # Validate schema on startup
    if not settings.validate_schema():
        raise Exception("Invalid schema configuration")

setup_cors(app)
