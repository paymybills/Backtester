"""
Python web server to serve the React frontend and provide API endpoints.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import the backend API
from backend import app as api_app

# Create main app
app = FastAPI(title="Backtesting Engine", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the API
app.mount("/api", api_app)

# Serve static files (React build)
if os.path.exists("dist"):
    app.mount("/static", StaticFiles(directory="dist"), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("dist/index.html")
    
    @app.get("/{path:path}")
    async def serve_frontend_routes(path: str):
        file_path = f"dist/{path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("dist/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)