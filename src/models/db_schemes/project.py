from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] =Field(None, alias ="_id")
    project_id: str =Field(..., max_length=1)   #  ولكن الطول 1 اقل شيئdefault بقوله ب 3 نقط دول خد كل ال 

    @field_validator('project_id')
    def validate_project_id(cls, value):           # الخاص بياvalidator هنا بنشأ ال
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        
        return value
    
        # 2. استخدم model_config بدلاً من class Config
    model_config = ConfigDict(arbitrary_types_allowed=True) #that for pydantic v2

    # class config:                      #that for pydantic v1
    #     arbitrary_types_allowed = True # object_idمش عارفة تعمل اي مع النوع الجديد pydantic هنامكتبة
                                 # ولذالك بعرف المتغير ده وبقولها لو لقيتي نوع غريب عليك متعمليش ايرور 
