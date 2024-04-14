import os
from fastapi import FastAPI
from databases import Database

app = FastAPI()

# 환경변수에서 데이터베이스 설정 읽기
DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 데이터베이스 URL 구성
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()

# Database 객체 생성
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    # 데이터베이스에 연결
    await database.connect()
    print("데이터베이스 연결 성공")

@app.on_event("shutdown")
async def shutdown():
    # 데이터베이스 연결 해제
    await database.disconnect()
    
@app.get("/databases")
async def list_databases():
    query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
    rows = await database.fetch_all(query)
    return {"databases": [row["datname"] for row in rows]}
