from pydantic import BaseModel, Field
from typing import Dict, Optional

class Info(BaseModel):
    taskId: str  
    taskName: str  
    select_sql: Optional[str] = Field(None, alias='select.sql', n)
    inCharge: str
    startDate: str
    unSuccessOverTime: str