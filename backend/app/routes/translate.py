from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slang
from app.schemas import SlangRequest, SlangResponse
from app.services.openai_service import translate_with_openai

router = APIRouter()

@router.post("/", response_model=SlangResponse)
def translate_word(request: SlangRequest, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word == request.word, Slang.approved == True).first()
    
    if slang:
        return {"word": slang.word, "translation": slang.translation}
    
    # OpenAI API 호출
    translated_text = translate_with_openai(request.word)

    # 새로운 번역을 DB에 저장
    new_slang = Slang(word=request.word, translation=translated_text, initial=request.word[0], approved=False)
    db.add(new_slang)
    db.commit()
    
    return {"word": request.word, "translation": translated_text}

