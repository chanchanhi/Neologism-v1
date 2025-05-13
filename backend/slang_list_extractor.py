# slang_list_extractor.py
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Slang

def get_slang_words():
    db: Session = SessionLocal()
    slang_words = [s.word for s in db.query(Slang).all()]
    db.close()
    return slang_words

if __name__ == "__main__":
    words = get_slang_words()
    with open("slang_vocab.txt", "w", encoding="utf-8") as f:
        for w in words:
            f.write(w + "\n")
    print(f"{len(words)}개의 신조어가 저장되었습니다.")