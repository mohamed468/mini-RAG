from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from routes import base, data, nlp
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.LLMInterface import LLMInterface #   استدعينا الانترفيس بتاعنا
from typing import Any
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.vectordb.VectorDBInterface import VectorDBInterface
from stores.llm.templates.template_parser import TemplateParser

# =================================================================
#   كلاس مخصص يورث FastAPI ونعرف فيه متغيراتنا
# =================================================================
class MiniRAGApp(FastAPI):
    mongo_conn: AsyncIOMotorClient
    db_client: Any 
    generation_client: LLMInterface # Pylance هيعرف إن ده بيعمل Generate
    embedding_client: LLMInterface  #  وهنا بيعمل Embed
    vectordb_client: VectorDBInterface
    template_parser: TemplateParser

@asynccontextmanager
async def lifespan(app: MiniRAGApp): #  غيرنا النوع هنا للكلاس بتاعنا
    try:
        print(" Starting up application.")
        settings = get_settings()
        
        # MongoDB Connection
        app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL) 
        app.db_client = app.mongo_conn[settings.MONGODB_DATABASE] 
        print(" MongoDB connected")
        
        # LLM Provider Factory
        llm_provider_factory = LLMProviderFactory(settings)
        
        vectordb_provider_factory = VectorDBProviderFactory(settings)

        # Generation Client
        app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND or "") 
        app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID or "")
        print(f" Generation client initialized ({settings.GENERATION_BACKEND})")
        
        # Embedding Client
        app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND or "") 
        app.embedding_client.set_embedding_model(
            model_id=settings.EMBEDDING_MODEL_ID or "",
            embedding_size=settings.EMBEDDING_MODEL_SIZE or 768
        )
        print(f" Embedding client initialized ({settings.EMBEDDING_BACKEND})")
        
        # Vector db client

        app.vectordb_client = vectordb_provider_factory.create(
            provider = settings.VECTOR_DB_BACKEND or "" # type: ignore
        )
        app.vectordb_client.connect()
        print(f"VectorDB client initialized ({settings.VECTOR_DB_BACKEND})")
        
        app.template_parser= TemplateParser(
            language=settings.PRIMARY_LANG,
            default_language= settings.DEFAULT_LANG,
        )

        yield  
        
    except Exception as e:
        print(f" Startup error: {e}")
        raise
    
    finally:
        print(" Shutting down application...")
        try:
            app.mongo_conn.close() 
            print(" MongoDB connection closed")
        except Exception as e:
            print(f" Shutdown error: {e}")
        try:
            if hasattr(app, 'vectordb_client'):

                app.vectordb_client.disconnect()
                print("VectorDB connection closed")
        except Exception as e:
            print(f"VectorDB Shutdown error: {e}")


# استخدام الكلاس المخصص بتاعنا بدل FastAPI العادي

app = MiniRAGApp(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

@app.get("/", include_in_schema=False)
def root():
    return {"message":"API is running"}