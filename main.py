# coding:utf-8
import uvicorn
from fastapi import FastAPI, Form
from replit import db
import time
import os


app = FastAPI(docs_url=None, redoc_url=None)


db["time"] = int(time.time())


try:
  del db["access_token"]
  del db["access_tokennew"]
  del db["refresh_tokennew"]
except:
  pass


# 帮我写一个入口函数
@app.get("/get")
def get_use_key():
  time_now = db["time"]
  split_time = int(time.time()) - time_now
  print(f"当前秘钥已使用 {split_time} 秒 ({split_time}/{4500-split_time})")
  if split_time < 4500:
    _value = db.get("access_token")
    print("从数据库中获取到 Access_Token")
  else:
    _value = None
    del db["access_token"]
    db["time"] = int(time.time())
    print("缓存超时！重新获取！")
  return _value


@app.get("/fresh")
def get_fresh_key():
    try:
      my_secret = db['refresh_token']
      print("从数据库中获取到 Refresh_Token")
    except:
      my_secret = os.environ['refresh_token']
      print("从环境变量中获取到 Refresh_Token")
    print("成功获取到刷新令牌")
    return my_secret


@app.post("/post_ak")
def post_temp_ak_new(name: str = Form(...), ak: str = Form(...)):
  db[name] = ak
  print(f"成功将{name}放置数据库")
  return "post sucess"


@app.get("/")
def root():
  db_list = db.keys()
  return {"Hello": db_list}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
