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
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/data")
async def fetch_data():
    query = 'SELECT * FROM "test-table"'
    result = await database.fetch_all(query)
    return {"data": result}

@app.get("/tables")
async def list_tables():
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    rows = await database.fetch_all(query)
    return {"tables": [row["table_name"] for row in rows]}

@app.post("/add-contact")
async def add_contact():
    query = """
    INSERT INTO "test-table" ("이름", "주소", "전화번호")
    VALUES ('박기자', '중동', '010-2959-1111');
    """
    await database.execute(query)
    return {"status": "Contact added successfully"}
