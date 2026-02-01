from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

# Import database and router
from app.database import create_db
from app.routes.user import router  # Import router from user.py

app = FastAPI(title="User Management System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_db()
    print("✅ Database initialized")

# Include users router
app.include_router(router)

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
                    <p>Make sure index.html is in the same directory as main.py</p>
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
        "database": "database.db"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting User Management System...")
    print("📁 Current directory:", os.getcwd())
    print("📄 Your files:")
    for file in os.listdir('.'):
        print(f"  - {file}")
    if os.path.exists('app'):
        print("📁 Files in app directory:")
        for file in os.listdir('app'):
            print(f"  - {file}")
    print("🌐 Server will run at: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)