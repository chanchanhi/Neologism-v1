from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slang
from app.schemas import SlangUpdate, SlangCreate
from app.utils import get_korean_initial

router = APIRouter()

@router.get("/search")
def search_word(word: str, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word.contains(word), Slang.approved == True, Slang.pending_delete == False).all()
    return [{"word": s.word, "translation": s.translation, "initial": get_korean_initial(s.word)} for s in slang]

@router.post("/update")
def update_word(request: SlangUpdate, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word == request.word).first()
    if slang:
        slang.pending_translation = request.translation
        slang.approved = False # 수정되었으므로 다시 승인 대기로 전환
        db.commit()
        return {"message": "수정 요청이 저장되었습니다. 관리자의 승인을 기다려주세요."}
    return {"message": "신조어를 찾을 수 없습니다"}


@router.post("/add")
def add_word(request: SlangCreate, db: Session = Depends(get_db)):
    # ✅ 중복 확인
    existing_word = db.query(Slang).filter(Slang.word == request.word).first()
    if existing_word:
        raise HTTPException(status_code=400, detail="이미 존재하는 신조어입니다.")

    # ✅ 초성 추출 후 저장
    initial = get_korean_initial(request.word)
    new_slang = Slang(word=request.word, translation="", pending_translation=request.translation, approved = False, initial=initial)
    
    db.add(new_slang)
    db.commit()

    return {"message": "신조어 추가 요청이 관리자에게 전달되었습니다!"}

# ✂️ 삭제 기능 추가
@router.delete("/delete/{word}")
def delete_slang(word: str, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.word == word).first()
    if not slang:
        raise HTTPException(status_code=404, detail="해당 신조어를 찾을 수 없습니다.")
    slang.pending_delete = True
    slang.approved = False  # 삭제 중이면 사용자에게도 숨김
    db.commit()
    return {"message": f"{word} 삭제 요청이 관리자에게 전달되었습니다."}
