from pydantic import BaseModel, Field
from typing import Dict, Optional

class Info(BaseModel):
    taskId: str  
    taskName: str  
    select_sql: str = Field(None, alias='select.sql', description="中文注释")
    inCharge: str
    startDate: str
    unSuccessOverTime: str



if __name__ == "__main__":
    data = {
        "taskId": "12",
        "taskName": "12",
        "inCharge": "12",
        "startDate": "345",
        # "select.sql":"123",
        "unSuccessOverTime": "12"
    }
    info = Info(**data)
    print(info)
