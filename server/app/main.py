"""Main FastAPI application setup with database"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.ping import router as ping_router
from app.api.routes.user import router as users_router
from app.api.routes.rides import router as rides_router
from app.database.connection import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        description="A modular FastAPI-based Mini-Uber project with PostgreSQL integration"
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
    app.include_router(ping_router)
    app.include_router(users_router)
    app.include_router(rides_router)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Mini-Uber API with PostgreSQL",
            "version": settings.version,
            "database": "PostgreSQL Connected"
        }

    return app


app = create_application()