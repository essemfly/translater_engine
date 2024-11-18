import json
import os
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from openai import BaseModel

from app.external.langchain_client import translate_text
from app.modules.google_document import GoogleDocument
from app.modules.load_pdf import load_pdf_all
from app.modules.save_translated_pdf import save_pdf
from app.modules.translate_text import replace_text_in_box
from app.utils.dimension import (
    get_paragraph_text,
    get_rect_from_paragraph,
)


app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application with SQLAlchemy and Alembic.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # 모든 도메인에 대해 허용. 필요한 경우 특정 도메인으로 제한 가능.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


from app.https.translate import pdf_router

app.include_router(pdf_router)
