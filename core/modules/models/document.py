from sqlalchemy import Column, Integer, String, create_engine, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    filename = Column(String)
    text = Column(String)


class DocumentPage(Base):
    __tablename__ = "document_pages"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    page_number = Column(Integer)
    text = Column(String)


class DocumentLineTranslation(Base):
    __tablename__ = "document_line_translations"

    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(Integer, index=True)
    from_lang = Column(String)
    to_lang = Column(String)
    text = Column(String)
    translation = Column(String)
    source = Column(String)


class DocumentLine(Base):
    __tablename__ = "document_lines"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, index=True)
    line_idx = Column(Integer)
    text = Column(String)
    startIndex = Column(Integer)
    endIndex = Column(Integer)
    translation = Column(String)
    translation_candidates = Column(ARRAY(DocumentLineTranslation))
