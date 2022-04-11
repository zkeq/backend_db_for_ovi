# coding:utf-8
import uvicorn
from fastapi import FastAPI
from replit import db
import time
import os

try:
  my_secret = db['refresh_token']
except:
  my_secret = os.environ['refresh_token']

app = FastAPI(docs_url=None, redoc_url=None)


db["time"] = int(time.time())

# 帮我写一个入口函数
@app.get("/get")
def get_use_key():
  time_now = db["time"]
  split_time = int(time.time()) - time_now
  print(f"当前延迟{split_time}")
  if split_time < 4500:
    _value = db.get("access_token")
    print("成功获取到缓存数据！")
  else:
    _value = None
    del db["access_token"]
    db["time"] = int(time.time())
    print("缓存超时！重新获取！")
  return _value


@app.get("/fresh")
def get_fresh_key():
    print("成功获取到刷新令牌")
    return my_secret

@app.get("/post_ak")
def post_temp_ak(name: str = None, ak: str = None):
  db[name] = ak
  print(f"成功将{name}放置数据库")
  return "suceess"


@app.get("/")
def root():
  db_list = db.keys()
  return {"Hello": db_list}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
