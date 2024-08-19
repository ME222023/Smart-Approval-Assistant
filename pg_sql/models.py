# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DateTime, ForeignKey, Integer, String, text
from pg_sql.database import Base, engine
metadata = Base.metadata



class ApprovalEvent(Base):
    __tablename__ = 'approval_event'
    __table_args__ = {'comment': '审批请求事件'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='事件ID')
    applicant = Column(String(20), nullable=False, comment='申请人oa帐号')
    admin = Column(String(20), nullable=False, comment='审批人admin_oa帐号')
    status = Column(CHAR(1), nullable=False, server_default=text("'P'"), comment='F: fished; P:preparation')


class EventTaskMap(Base):
    __tablename__ = 'event_task_map'
    __table_args__ = {'comment': '审批请求事件与task映射表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增ID')
    event_id = Column(Integer, nullable=False, comment='事件ID')
    task_id = Column(String(20), nullable=False, comment='任务ID')


class AdminInfo(Base):
    __tablename__ = 'admin_info'
    __table_args__ = {'comment': '纪录Admin的oa账户对应的userid'}

    oa = Column(String(20), primary_key=True, comment='oa帐号')
    userid = Column(String(100), nullable=True, comment='用户签标')
    enabled = Column(CHAR(1), nullable=False, server_default=text("'1'"), comment='1: 可用，0：不可用 ')


if __name__ == "__main__":
    Base.metadata.create_all(engine)