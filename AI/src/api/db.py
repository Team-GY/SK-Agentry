from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from dotenv import load_dotenv
import os


# .env 로드
load_dotenv(dotenv_path="../.env")

# 환경 변수에서 MySQL 접속 정보 가져오기
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")

DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)


# ✅ 비동기 데이터베이스 엔진 생성
async_engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ 비동기 세션 팩토리 설정
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ✅ 비동기 지원을 위한 SQLAlchemy 기본 클래스
Base = declarative_base(cls=AsyncAttrs)  # ✅ AsyncAttrs 추가

# ✅ 비동기 데이터베이스 세션을 반환하는 종속성 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # ✅ 비동기 세션 반환 (async with 사용)
