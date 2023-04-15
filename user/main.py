from app import router as AppsRoute
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

app = FastAPI()
# @app.get('/')
# def  read_root():
#     return {"hello":"World"}

app.include_router(AppsRoute.router)

register_tortoise(app,
                  db_url = "postgres://postgres:root@127.0.0.1/crud_fastapi",
                  modules =  {"models":['app.models',]},
                  generate_schemas = True,
                  add_exception_handlers = True
                  )