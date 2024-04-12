from databases import Database
from fastapi import FastAPI

# 데이터베이스 URL 설정
DATABASE_URL = "postgresql-test:5432"

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
