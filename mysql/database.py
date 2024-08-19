from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# pip install sqlalchemy mysqlclient aiomysql pymysql
MYSQL_DATABASE_URL ="mysql://gpt_cx:gpt##2024@10.5.98.170:3306/lhotsetest"

engine = create_engine(
    # 使用sqlite3需要用的参数
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    MYSQL_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()