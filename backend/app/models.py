from sqlalchemy import Column, String, Integer, Text, Boolean
from app.database import Base

class Slang(Base):
    __tablename__ = "slang_dictionary"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, index=True, nullable=False)
    translation = Column(Text, nullable=False)
    pending_translation = Column(Text, nullable=True)  # ✅ 수정 제안 보관용
    pending_delete = Column(Boolean, default=False)  # ✅ 삭제 요청 여부
    initial = Column(String(10), nullable=False)  # 초성 저장
    approved = Column(Boolean, default=False) # 승인 여부 필드 추가
