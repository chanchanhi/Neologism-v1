from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import translate, dictionary, admin
from app.database import engine, Base
from app.routes import admin_auth

app = FastAPI(title="GPT 신조어 번역기 API")

# ✅ CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 서버가 시작될 때 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 번역 및 사전 API 라우트 등록
app.include_router(translate.router, prefix="/translate", tags=["Translate"])
app.include_router(dictionary.router, prefix="/dictionary", tags=["Dictionary"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])  # ✅ 관리자 라우터
app.include_router(admin_auth.router)

@app.get("/")
def root():
    return {"message": "신조어 번역 API 작동 중"}

# FastAPI 실행 명령
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
