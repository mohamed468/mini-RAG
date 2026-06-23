from typing import List
import uuid
from qdrant_client import models , QdrantClient
from ..VectorDBInterface import VectorDBInterface
import logging
from ..VectorDBEnums import DistanceMethodEnums
from typing import List
from qdrant_client.http import models
from models.db_schemes import RetrivedDocument

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path:str, distance_method: str):
        self.client: QdrantClient | None = None
        self.db_path = db_path
        self.distance_method = models.Distance.COSINE
        
        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE

        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path = self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name= collection_name) # type: ignore 
    
    def list_all_collections(self)-> List:
        return self.client.get_collections().collections # type: ignore
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name = collection_name).model_dump() # type: ignore
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name= collection_name) # type: ignore
    
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        if do_reset:
           _ = self.delete_collection(collection_name= collection_name)

        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection( # type: ignore
                collection_name = collection_name,
                vectors_config= models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True
        
        return False
    
    def insert_one(self, collection_name: str, text: str, vector: List, metadata: dict | None = None, record_id: str | None = None):
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"can not isert new record to non-existed collection : {collection_name}")
            return False
        _id = record_id if record_id else str(uuid.uuid4())

        try:
            _ = self.client.upsert( # type: ignore
                collection_name = collection_name,
                points =[
                    models.PointStruct(
                    id=_id,
                    vector = vector,
                    payload = {
                        "text": text , "metadata" : metadata            }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting batch : {e}")
            return False

        return True
    
    def insert_many(self, collection_name: str, texts: List, vectors: List, metadata: List | None = None, record_ids: List | None = None, batch_size: int = 50):
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range( 0, len(texts)))    

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]
            
            points = [
                models.PointStruct(
                    id = batch_record_ids[x],
                    vector = batch_vectors[x],
                    payload = {
                        "text" : batch_texts[x], "metadata" : batch_metadata[x]
                    }
                )

                for x in range(len(batch_texts))
            ]  
            try: 
                _ = self.client.upsert( # type: ignore
                    collection_name = collection_name,
                    points=points
                )
            except Exception as e:
                self.logger.error(f"Error while insrting batch:{e}")
                return False

        return True

    def search_by_vector(self, collection_name: str, vector: List, limit: int = 5):
        response = self.client.query_points( # type: ignore
            collection_name=collection_name,
            query=vector, 
            limit=limit,
            with_payload=True
        )
        
        # 1. نستخرج قائمة النتائج (List) من الكائن اللي راجع
        results = response.points 
        
        if not results or len(results) == 0:
            return None
        
        return [
            RetrivedDocument(**{
                "score": result.score,
                # 2. حماية إضافية: نتأكد إن الـ payload مش None قبل ما نقرأ منه النص
                "text" : result.payload["text"] if result.payload else "", 
            })
            for result in results
        ]
                    
    
