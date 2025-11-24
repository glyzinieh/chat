from fastapi import FastAPI

app = FastAPI()


from app.api import router

app.include_router(router)
