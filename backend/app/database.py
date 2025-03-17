from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os

DATABASE_URL = "mysql+pymysql://slanguser:slangpass@db/slangdb"

# MySQL이 준비될 때까지 대기
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        break
    except Exception as e:
        print(f"MySQL 연결 실패, 재시도 중... ({i+1}/10)")
        time.sleep(3)  # 3초 대기 후 다시 시도
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

