from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnums import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne        #batch/bulk write هحتاج دا في عملية ال  

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client= db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk : DataChunk):
            result = await self.collection.insert_one(chunk.dict(by_alias = True, exclude_unset= True))
            chunk._id = result.inserted_id
            return chunk
    
    #str واول ما يخرج يتحول ل objectidهيتحول ل mongo اول ما يدخل id هناال 
    async def get_chunk (self, chunk_id: str): 
         result = await self.collection.find_one(    #asyncioدا collectionعشان الawaitهيدور على حاجة وعملت 
              {
                   "_id" : ObjectId(chunk_id)  # ولما يلاقيها يحولها للنوع دا id هيدور هنا على ال 
              }
         )

         if result is None:
              return None
         # **وهنا الresultجديدة واديهاالDataChunkهنا هعمل 
         #paramters ل Dictionaryهتفق ال 
         return DataChunk(**result) 
        
    async def insert_many_chunks(self, chunks:list, batch_size:int=100):
         for i in range(0, len(chunks) , batch_size): #هنا هيبدا من0وصولاالي العددالكلي وكل مرةيمشي  كذا
            batch = chunks[i:i+batch_size]

            operations = [                 #Insertهنا بعرف عملية ال 
                 InsertOne(chunk.dict(by_alias = True, exclude_unset= True))   #2. dict الى chunkجهز العملية بأنك تحول ال 
                 for chunk in batch        #1.  batchفي الchunkهقول هنا لكل 
            ]

            #ال جهزتهالهoperationsواديله bulkهنا بنادي ال 
            await self.collection.bulk_write(operations)

         return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id : ObjectId):
         result = await self.collection.delete_many({
              "chunk_project_id" : project_id
         })

         return result.deletet_count
         

    