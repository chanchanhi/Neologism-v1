from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slang

router = APIRouter()

# ① 승인 대기 목록 조회
@router.get("/pending")
def get_pending_slangs(db: Session = Depends(get_db)):
    pending = db.query(Slang).filter((Slang.approved == False) | (Slang.pending_delete == True)).all()
    result = []
    for slang in pending:
        # 요청 유형 판별
        if slang.pending_delete:
            request_type = "삭제 요청"
        elif slang.translation == "":
            request_type = "신규 등록"
        elif slang.pending_translation:
            request_type = "뜻 수정 요청"
        else:
            request_type = "알 수 없음"

        result.append({
            "id": slang.id,
            "initial": slang.initial,
            "word": slang.word,
            "translation": slang.translation,
            "pending_translation": slang.pending_translation,
            "pending_delete": slang.pending_delete,
            "request_type": request_type
        })

    return result

# ② 특정 단어 승인
@router.post("/approve/{slang_id}")
def approve_slang(slang_id: int, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.id == slang_id).first()
    if not slang:
        raise HTTPException(status_code=404, detail="해당 신조어를 찾을 수 없습니다.")

    if slang.pending_delete:
        # 삭제 요청 승인
        db.delete(slang)
        db.commit()
        return {"message": f"{slang.word} 삭제 요청 승인 완료!"}

    else:
        # 신규 or 수정 요청 승인
        if slang.pending_translation:
            slang.translation = slang.pending_translation
            slang.pending_translation = None
        slang.approved = True
        slang.pending_delete = False
        db.commit()
        return {"message": f"{slang.word} 승인 완료!"}

# ✅ 승인 요청 거절
@router.post("/reject/{slang_id}")
def reject_request(slang_id: int, db: Session = Depends(get_db)):
    slang = db.query(Slang).filter(Slang.id == slang_id).first()
    if not slang:
        raise HTTPException(status_code=404, detail="해당 신조어를 찾을 수 없습니다.")

    if not slang.approved and slang.pending_translation and not slang.pending_delete:
        # 신규 등록 거부
        if slang.translation == "":
            db.delete(slang)
            db.commit()
            return {"message": "신규 단어 등록 요청이 거부되었습니다."}
        else:
            # 뜻 수정 요청 거부
            slang.pending_translation = None
            slang.approved = True
            db.commit()
            return {"message": "뜻 수정 요청이 거부되었습니다."}

    elif slang.pending_delete:
        # 삭제 요청 거부
        slang.pending_delete = False
        slang.approved = True
        db.commit()
        return {"message": "삭제 요청이 거부되었습니다."}

    return {"message": "거부할 요청이 없습니다."}
