from fastapi import FastAPI, Depends, HTTPException


app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application with SQLAlchemy and Alembic.",
    version="1.0.0",
)
