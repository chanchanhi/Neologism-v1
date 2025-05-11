from app.database import SessionLocal
from app.models import AdminUser
from app.utils import hash_password

db = SessionLocal()

admin = AdminUser(
    username="admin",
    password_hash=hash_password("pass123")
)

db.add(admin)
db.commit()
db.close()

print("✅ 관리자 계정 생성 완료!")
