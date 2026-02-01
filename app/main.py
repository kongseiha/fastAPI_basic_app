from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Import database and router
from app.database import create_db, engine, SessionLocal
from app.model import User
from app.routes.user import router
from sqlmodel import SQLModel, select

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

# Create database tables and add sample data on startup
@app.on_event("startup")
def startup_event():
    # Create tables
    SQLModel.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Add sample data
    with SessionLocal() as session:
        # Check if we have any users
        users = session.exec(select(User)).all()
        
        if not users:
            print("📝 Adding sample users...")
            sample_users = [
                User(name="John Doe", age=30, phone="1234567890", email="john@example.com"),
                User(name="Jane Smith", age=25, phone="0987654321", email="jane@example.com"),
                User(name="Bob Wilson", age=35, phone="5551234567", email="bob@example.com"),
                User(name="Alice Johnson", age=28, phone="4445556666", email="alice@example.com"),
                User(name="Charlie Brown", age=40, phone="7778889999", email="charlie@example.com"),
            ]
            
            for user in sample_users:
                session.add(user)
            
            session.commit()
            print(f"✅ Added {len(sample_users)} sample users")
        else:
            print(f"📊 Database has {len(users)} users")

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

# Health check endpoint with database info
@app.get("/health")
async def health_check():
    with SessionLocal() as session:
        user_count = len(session.exec(select(User)).all())
    
    return {
        "status": "healthy", 
        "message": "User Management API is running",
        "database": "SQLite",
        "users_count": user_count,
        "note": "SQLite is ephemeral on Render free tier"
    }