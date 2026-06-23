from pydantic import BaseModel, Field, field_validator , ConfigDict
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    model_config = ConfigDict(# ← الأفضل يكون الأول
        arbitrary_types_allowed=True,
        populate_by_name=True
        )                 #that for pydantic v2
    #'_' يبدا ب id هنا في مشكلة أن ال
    # Aliasومينفعش حد يأكسس عليه من برا ولذالك الحل في عمل private فمعنى كده انه 
    id: Optional[ObjectId] =Field(default=None, alias="_id")
    chunk_text: str   =Field(..., min_length=1)
    chunk_metadata : dict
    chunk_order: int  =Field(..., gt=0)
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId
    
    # class config:
    #     arbitrary_types_allowed = True  #that for pydantic v1

    @classmethod
    def get_indexes (cls):
        return [
            {
                "key" : [
                    ("chunk_project_id", 1)
                ],
                "name" : "chunk_project_id_index_1",
                "unique" : False
            }
        ]

class RetrivedDocument(BaseModel):
    text: str
    score: float
    