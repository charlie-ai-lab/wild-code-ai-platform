"""
FastAPI Main Application
野码AI Agent协作平台
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.agents import router as agents_router
from api.tasks import router as tasks_router

app = FastAPI(
    title="野码AI Agent Platform",
    version="0.1.0",
    description="统一的多AI Agent协作平台"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {
        "message": "野码AI Agent Platform API",
        "version": "0.1.0",
        "status": "developing",
        "docs": "/docs",
        "endpoints": {
            "agents": "/agents",
            "tasks": "/tasks",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "agent-platform"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
