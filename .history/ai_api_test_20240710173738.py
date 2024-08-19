from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StringArray(BaseModel):
    items: List[str]

@app.post("/str/")
async def process_strings(tasks_id: StringArray):
    # 这里你可以处理接收到的字符串数组
    processed_data = {"received_items": tasks_id}
    return processed_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=28000, res)