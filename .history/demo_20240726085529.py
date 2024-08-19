from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

# 连接到本地 Redis 服务器
r = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/popr/{id}")
async def popr(id: str):
    # 获取队列中的值
    value = r.lpop(id)
    
    if value is None:
        # 如果队列为空，返回错误信息
        raise HTTPException(status_code=404, detail="error")
    
    # 返回弹出的值
    return {"value": value.decode('utf-8')}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
