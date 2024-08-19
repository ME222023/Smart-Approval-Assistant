# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DateTime, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from mysql.database import Base

metadata = Base.metadata


class LbApproval(Base):

    __tablename__ = 'lb_approval'

    id = Column(Integer, primary_key=True, comment='id主键')
    task_id = Column(String(20), nullable=False, comment='任务ID')
    applicant = Column(String(50), nullable=False, comment='申请人')
    applicant_time = Column(String(2000), nullable=False, comment='申请时间')
    approval = Column(String(50), nullable=False, comment='审批人')
    approval_comment = Column(String(2000), nullable=False, comment='审批意见')
    approval_result = Column(String(30), comment='审批结果')
    approval_status = Column(String(100), nullable=False, comment='审批状态')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class LbTaskType(Base):
    __tablename__ = 'lb_task_type'
    __table_args__ = {'comment': '任务类型'}

    type_id = Column(SmallInteger, primary_key=True, comment='类型ID')
    type_desc = Column(String(100), nullable=False, comment='类型描述')
    type_sort = Column(String(100), nullable=False, comment='所属大类')
    in_charge = Column(String(30), nullable=False, comment='负责人')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    killable = Column(TINYINT, nullable=False, server_default=text("'0'"), comment='未找到实际用途')
    retry_wait = Column(BigInteger, nullable=False, server_default=text("'10'"), comment='重试间隔，未实际生效')
    broker_parallelism = Column(BigInteger, nullable=False, server_default=text("'10'"), comment='同一个执行器节点的最高并发')
    task_parallelism = Column(BigInteger, nullable=False, server_default=text("'5'"), comment='单个任务并发数，未实际生效')
    polling_seconds = Column(BigInteger, nullable=False, server_default=text("'10'"), comment='未找到实际用途')
    param_list = Column(VARCHAR(200), server_default=text("' '"), comment='未找到实际用途')


class LbTopic(Base):
    __tablename__ = 'lb_topic'
    __table_args__ = {'comment': '主题表'}

    topic_name = Column(String(32), primary_key=True, comment='topic名称')
    topic_desc = Column(String(30), nullable=False, comment='topic描述')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    dept_name = Column(String(32))
    topic_in_charge = Column(String(32))


class LbTask(Base):
    __tablename__ = 'lb_task'
    __table_args__ = {'comment': '任务配置表'}

    task_id = Column(CHAR(17), primary_key=True, comment='任务ID')
    task_type = Column(ForeignKey('lb_task_type.type_id'), nullable=False, index=True, comment='类型ID')
    task_name = Column(String(128), unique=True, comment='任务描述')
    broker_ip = Column(String(20), nullable=False, server_default=text("'any'"), comment='broker机器IP')
    server_tag = Column(String(500), comment='服务器标识(,分隔)')
    cycle_unit = Column(CHAR(1), nullable=False, comment='周期单位(M/W/D/H/I)')
    cycle_num = Column(SmallInteger, nullable=False, server_default=text("'1'"), comment='周期数')
    start_date = Column(DateTime, nullable=False, comment='开始日期')
    end_date = Column(DateTime, comment='截止日期')
    self_depend = Column(SmallInteger, nullable=False, server_default=text("'1'"), comment='自身依赖(1-时序/2-非时序/3-并行)')
    task_action = Column(String(255), nullable=False, comment='任务执行目标')
    try_limit = Column(Integer, nullable=False, server_default=text("'3'"))
    delay_time = Column(SmallInteger, nullable=False, server_default=text("'0'"), comment='延迟时间(分)')
    startup_time = Column(SmallInteger, nullable=False, server_default=text("'0'"), comment='启动时间(分)')
    alive_wait = Column(SmallInteger, nullable=False, server_default=text("'30'"), comment='最长存活等待(分钟)')
    retriable = Column(SmallInteger, nullable=False, server_default=text("'1'"), comment='失败可重试(0-否)')
    status = Column(CHAR(1), nullable=False, server_default=text("'Y'"), comment='状态(F:冻结/C:草稿/Y:正常/N:删除)')
    task_priority = Column(SmallInteger, nullable=False, server_default=text("'0'"), comment='优先级(0,1,2,3)')
    task_group = Column(String(255), comment='所属组')
    notes = Column(String(1000), comment='备注')
    in_charge = Column(String(2000))
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    old_id = Column(String(100), comment='旧任务ID(复制用)')
    source_server = Column(String(100))
    target_server = Column(String(100))
    topic_name = Column(String(32), server_default=text("''"), comment='主题名称')
    module_name = Column(String(32), server_default=text("''"), comment='模块名称')
    runOverTime = Column(SmallInteger, server_default=text("'0'"), comment='任务运行超时时间(单位:分钟,0表示没有限制)')
    unSuccessOverTime = Column(SmallInteger, server_default=text("'0'"), comment='最大没运行时间(超过则发出报警)')
    schedule_type = Column(CHAR(1))
    data_type = Column(CHAR(1))
    task_desc = Column(String(255))
    update_by = Column(String(100))
    upddate_date = Column(DateTime)
    unRunOverTime = Column(SmallInteger, server_default=text("'0'"), comment='任务到点未运行告警时间(单位:分钟,0表示没有限制)')
    advance_init = Column(TINYINT(1), server_default=text("'0'"), comment='是否收市后实例化')
    developer = Column(String(255))
    ait_tables = Column(String(255), comment='目标表')
    source_tables = Column(String(255), comment='来源表')
    exe_environment = Column(SmallInteger, server_default=text("'0'"), comment='任务运行环境,0-交易网,1-办公网')

    lb_task_type = relationship('LbTaskType')
