from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Import database and router
from app.database import create_db
from app.routes.user import router

app = FastAPI(
    title="User Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_db()
    print("✅ Database initialized")

# Include users router
app.include_router(router)

# Serve static files for Render
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve HTML file
@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content=f"""
            <html>
                <body style="font-family: Arial; padding: 40px; text-align: center;">
                    <h1>⚠️ index.html not found</h1>
                    <p>Current directory: {os.getcwd()}</p>
                    <p>Files available: {', '.join(os.listdir('.'))}</p>
                </body>
            </html>
            """,
            status_code=404
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "User Management API is running",
        "service": "fastapi_basic_app",
        "environment": os.getenv("RENDER", "development")
    }

# Only run with uvicorn directly in development
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting in development mode...")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )