from databases import Database
from fastapi import FastAPI

# 데이터베이스 URL 설정
DATABASE_URL = "postgresql://user:password@host:port/database_name"

app = FastAPI()

@app.on_event("startup")
async def startup():
    # 데이터베이스에 연결
    await database.connect()
    print("데이터베이스 연결 성공")

@app.on_event("shutdown")
async def shutdown():
    # 데이터베이스 연결 해제
    await database.disconnect()
