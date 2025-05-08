from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs

# ✅ MySQL 비동기 데이터베이스 URL
# ASYNC_DB_URL = "mysql+aiomysql://manager@db:3306/demo?charset=utf8mb4"
ASYNC_DB_URL = "mysql+aiomysql://manager:SqlDba-1@0.0.0.0:53303/demo?charset=utf8mb4"

# ✅ 비동기 데이터베이스 엔진 생성
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

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
