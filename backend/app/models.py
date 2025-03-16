from sqlalchemy import Column, String, Integer
from app.database import Base

class Slang(Base):
    __tablename__ = "slang_dictionary"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, index=True, nullable=False)
    translation = Column(String(255), nullable=False)
    initial = Column(String(10), nullable=False)  # 초성 저장
