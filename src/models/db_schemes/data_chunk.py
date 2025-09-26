from pydantic import BaseModel, Field, field_validator , ConfigDict
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    #'_' يبدا ب id هنا في مشكلة أن ال
    # Aliasومينفعش حد يأكسس عليه من برا ولذالك الحل في عمل private فمعنى كده انه 
    id: Optional[ObjectId] =Field(None, alias ="_id")
    chunk_text: str =Field(..., min_length=1)
    chunk_metadata : dict
    chunk_order: int =Field(..., gt=0)
    chunk_project_id: ObjectId



        # 2. استخدم model_config بدلاً من class Config
    model_config = ConfigDict(arbitrary_types_allowed=True)  #that for pydantic v2

    # class config:
    #     arbitrary_types_allowed = True  #that for pydantic v1
