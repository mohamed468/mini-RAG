# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient
# from helpers.config import get_settings
# from routes import base, data

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # --- Startup logic ---
#     settings = get_settings()
#     app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  # الاتصال بالـ MongoDB
#     app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]  # اختيار الداتابيز

#     try:
#         yield  # هنا التطبيق يشتغل
#     finally:
#         # --- Shutdown logic ---
#         app.mongo_conn.close()

# # استخدم الـ lifespan في إنشاء الـ app
# app = FastAPI(lifespan=lifespan)

# # Include Routers
# app.include_router(base.base_router)
# app.include_router(data.data_router)