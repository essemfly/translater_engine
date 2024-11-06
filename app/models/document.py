from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, ARRAY
from sqlalchemy.orm import relationship
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
    document_id = Column(
        Integer, ForeignKey("documents.id"), index=True
    )  # ForeignKey 추가
    page_number = Column(Integer)
    text = Column(String)

    document = relationship("Document", back_populates="pages")  # 관계 설정


class DocumentLineTranslation(Base):
    __tablename__ = "document_line_translations"

    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(
        Integer, ForeignKey("document_lines.id"), index=True
    )  # ForeignKey 추가
    from_lang = Column(String)
    to_lang = Column(String)
    text = Column(String)
    translation = Column(String)
    source = Column(String)

    line = relationship("DocumentLine", back_populates="translations")  # 관계 설정


class DocumentLine(Base):
    __tablename__ = "document_lines"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(
        Integer, ForeignKey("document_pages.id"), index=True
    )  # ForeignKey 추가
    line_idx = Column(Integer)
    text = Column(String)
    startIndex = Column(Integer)
    endIndex = Column(Integer)
    translation = Column(String)

    page = relationship("DocumentPage", back_populates="lines")  # 관계 설정
    translations = relationship(
        "DocumentLineTranslation", back_populates="line"
    )  # 관계 설정
