from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# pip install sqlalchemy mysqlclient aiomysql pymysql  psycopg2-binary
# POSTGRESQL_DATABASE_URL ="postgresql://root:2wsx!QAZ@localhost:port/weichat"
POSTGRESQL_DATABASE_URL ="postgresql://postgres:123456@postgres:5432/postgres"

engine = create_engine(
    # 使用sqlite3需要用的参数
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    POSTGRESQL_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import inspect
# 创建inspect对象
inspector = inspect(engine)

# 获取所有表信息
tables = inspector.get_table_names()
print(tables)
# 打印所有表信息
for table in tables:
    print(table)

