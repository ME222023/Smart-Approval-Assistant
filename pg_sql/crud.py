from sqlalchemy.orm import Session
from mysql.models import LbTask, LbApproval
import warnings
from sqlalchemy import exc as sa_exc

warnings.filterwarnings('ignore', category=sa_exc.SAWarning)


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

    pass