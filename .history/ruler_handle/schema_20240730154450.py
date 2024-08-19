
class Info(BaseModel):
    taskId: str  
    taskName: str  
    select_sql: Optional[str] = Field(None, alias='select.sql')
    inCharge: str
    startDate: str
    unSuccessOverTime: str