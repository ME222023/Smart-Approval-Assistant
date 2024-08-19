from sqlalchemy.orm import Session
from mysql.models import LbTask, LbApproval
import warnings
from sqlalchemy import exc as sa_exc

warnings.filterwarnings('ignore', category=sa_exc.SAWarning)


def get_task_info_by_applicant(db: Session, applicant, taskids=None, keyword=None):
    # 通过申请人applicant获取当前所有未审批，任务状态正常的task
    # LbTask.status	状态	char（1）	F': '禁用', 'C': '草稿', 'Y': '上线', 'N': '删除', 'W': '待审', 'A': '审核被拒', 'S': '其他'
    # approval_status	审批状态	varchar（100）	A已审批，W未审批
    _not_approval_status = "W"
    _not_approval_task_status = "W"
    if taskids is not None:
        querys = db.query(
            LbApproval.task_id,
            LbTask.task_name,
            LbApproval.applicant).filter(
                LbApproval.task_id == LbTask.task_id,
                        LbApproval.applicant == applicant,
                        LbTask.status == _not_approval_task_status,
                        LbApproval.task_id.in_(taskids),
                        LbApproval.approval_status == _not_approval_status).order_by(LbApproval.task_id).all()
    elif keyword is not None:
        querys = db.query(
            LbApproval.task_id,
            LbTask.task_name,
            LbApproval.applicant).filter(
                LbApproval.task_id == LbTask.task_id,
                        LbApproval.applicant == applicant,
                        LbTask.status == _not_approval_task_status,
                        LbTask.task_name.like(f'%{keyword}%'),
                        LbApproval.approval_status == _not_approval_status).order_by(LbApproval.task_id).all()
    else:
        querys = db.query(
            LbApproval.task_id,
            LbTask.task_name,
            LbApproval.applicant).filter(
                LbApproval.task_id == LbTask.task_id,
                        LbApproval.applicant == applicant,
                        LbTask.status == _not_approval_task_status,
                        LbApproval.approval_status == _not_approval_status).order_by(LbApproval.task_id).all()
    return querys



def modify_approval_result(db: Session, task_ids, approval, approval_result):
    # 查询需要修改的数据
    data_to_modify = db.query(LbApproval).filter(LbApproval.task_id.in_(task_ids)).all()

    # 修改数据的字段值
    for data in data_to_modify:
        data.approval = approval
        data.approval_comment = '审批通过' if approval_result else '审批不通过'
        data.approval_result = 'APPROVAL_PASSED' if approval_result else 'APPROVAL_NOT_PASSED'
        data.approval_status = 'A'
    db.commit()

#
# def create_tn_asset_inventory(db: Session, info):
#     db_info = models.TnAssetInventory(**info)
#     db.add(db_info)
#     db.commit()
#     db.refresh(db_info)
#     return db_info
#
#
# def create_tn_meta_dmod_info(db: Session, info):
#     print(f"create_tn_meta_dmod_info: \n{info}")
#     row_info = db.query(models.TnMetaDmodInfo).filter_by(dmod_en_name=info.get("dmod_en_name")).first()
#     if row_info is None:
#         db_info = models.TnMetaDmodInfo(**info)
#         db.add(db_info)
#         db.commit()
#         db.refresh(db_info)
#     else:
#         print(f"已经插入了{info.get('dmod_en_name')}")
#

if __name__ == "__main__":
    from mysql.database import SessionLocal
    db = SessionLocal()

    # querys = get_task_info_by_applicant(db, "zhangzh4", ["10002793"])
    querys = get_task_info_by_applicant(db, "guoyf2", keyword="repo_info_uat")
    from message_hander import approval_process_message
    print(approval_process_message(querys))