import os
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.websocket import websocket_router
from app.core.settings import Settings

load_dotenv()

settings = Settings()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    app.include_router(websocket_router)
    
    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    print(f"Application startup: {settings.APP_NAME} v{settings.APP_VERSION}")
    
@app.on_event("shutdown")
async def shutdown():
    print(f"Application is shutting down...")
    

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )