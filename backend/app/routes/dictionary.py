from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slang
from app.schemas import SlangUpdate
from app.utils import get_korean_initial

router = APIRouter()

@router.get("/search")
def search_word(word: str, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word.contains(word)).all()
    return [{"word": s.word, "translation": s.translation, "initial": get_korean_initial(s.word)} for s in slang]

@router.post("/update")
def update_word(request: SlangUpdate, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word == request.word).first()
    if slang:
        slang.translation = request.translation
        db.commit()
        return {"message": "번역이 수정되었습니다"}
    return {"message": "신조어를 찾을 수 없습니다"}

