from datetime import datetime
from sqlalchemy import String, Text, LargeBinary, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    text_data: Mapped[str] = mapped_column(Text, nullable=False)
    rec_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
