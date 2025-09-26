from typing import Union
from fastapi import FastAPI
# from dotenv import load_dotenv     # هستبدلهم بحاجة تانية
# load_dotenv(".env")
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from routes import base, data

app = FastAPI()
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()

    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)   # mongodbهنا حصلت على اتصال ب
    app.db_client= app.mongo_conn[settings.MONGODB_DATABASE] #mongoهنا حصلت على اتصال بالداتابيز الموجودةtd

@app.on_event("shutdown")

async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_router)
app.include_router(data.data_router)

