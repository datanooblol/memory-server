from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from package.routers.user import router as user_router
from package.routers.project import router as project_router
from package.routers.source import router as source_router
from package.routers.chat_session import router as chat_session_router
from package.routers.conversation import router as conversation_router
from package.routers.reference import router as reference_router

app = FastAPI(title="Memory Service")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in [
    user_router,
    project_router,
    source_router,
    chat_session_router,
    conversation_router,
    reference_router
]:
    app.include_router(r)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Memory API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)