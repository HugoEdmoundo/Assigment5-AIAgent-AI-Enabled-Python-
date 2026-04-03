from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from app.core.config import settings
from app.api.routes import tools, agent
from app.db.database import engine
from app.db import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Agent API with LiteLLM, Sessions, and Streaming",
    version="0.1.0",
    debug=settings.DEBUG,
    docs_url=None,  # Disable default Swagger
    redoc_url=None  # Disable ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])

@app.get("/")
async def root():
    return {
        "message": "AI Agent API is running",
        "docs": "/docs",
        "version": "0.1.0",
        "features": ["litellm", "sessions", "streaming", "tools"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Scalar API documentation
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
