"""
FastAPI Main Application
野码AI Agent协作平台
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="野码AI Agent Platform", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "野码AI Agent Platform API",
        "version": "0.1.0",
        "status": "developing",
        "endpoints": {
            "agents": "/agents",
            "skills": "/skills",
            "collaboration": "/collaboration",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agents")
async def list_agents():
    return {
        "agents": [
            {
                "id": "claude_code",
                "name": "Claude Code",
                "type": "ai_agent",
                "status": "active"
            },
            {
                "id": "gemini_cli",
                "name": "Gemini CLI",
                "type": "ai_agent",
                "status": "active"
            },
            {
                "id": "open_code",
                "name": "OpenCode",
                "type": "editor",
                "status": "active"
            },
            {
                "id": "codebuddy",
                "name": "CodeBuddy",
                "type": "assistant",
                "status": "active"
            }
        ]
    }

@app.get("/skills")
async def list_skills():
    return {
        "total": 50,
        "categories": {
            "ai_development": 12,
            "github_automation": 17,
            "search_tools": 6,
            "design_tools": 4,
            "financial_analysis": 1
        },
        "skills": [
            {"id": "github-action-gen", "name": "GitHub Action Generator", "category": "github_automation"},
            {"id": "ai-explain", "name": "AI Code Explainer", "category": "ai_development"},
            {"id": "github-kb", "name": "GitHub Knowledge Base", "category": "github_automation"},
            {"id": "github-pr", "name": "GitHub PR Tool", "category": "github_automation"},
            {"id": "claude_code", "name": "Claude Code", "category": "ai_development"},
            {"id": "gemini_cli", "name": "Gemini CLI", "category": "ai_development"},
            {"id": "open_code", "name": "OpenCode", "category": "editor"},
            {"id": "codebuddy", "name": "CodeBuddy", "category": "assistant"},
            {"id": "tavily-search", "name": "Tavily Search", "category": "search_tools"}
        ]
    }

@app.get("/collaboration")
async def list_collaboration_rooms():
    return {
        "active_rooms": 1,
        "rooms": [
            {
                "id": "room_1",
                "name": "Main Development Room",
                "participants": ["system", "developer"],
                "active_agents": ["claude_code"]
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
