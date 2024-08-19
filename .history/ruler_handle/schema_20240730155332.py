from pydantic import BaseModel, Field
from typing import Dict, Optional

class Info(BaseModel):
    taskId: str  
    taskName: str  
    select_sql: str = Field(None, alias='select.sql', description="中文注释")
    inCharge: str
    startDate: str
    unSuccessOverTime: str


__
if __name__ == "__":
    pass