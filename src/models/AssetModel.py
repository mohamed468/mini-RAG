from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .ProjectModel import Project
from .enums.DataBaseEnums import DataBaseEnum
from bson import ObjectId
from typing import Union ,Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase

class AssetModel(BaseDataModel):

    def __init__(self, db_client: AsyncIOMotorDatabase):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.CollECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: AsyncIOMotorDatabase):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.CollECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.CollECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        reslt = await self.collection.insert_one(
            asset.model_dump(by_alias=True, exclude_unset=True)
        )
        asset.id = reslt.inserted_id

        return asset

    async def get_all_project_assets(self, asset_project_id: Union[str, ObjectId], asset_type: str):
        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type
        }).to_list(length=None)

        return [
            Asset(**record)
            for record in records
        ]

    async def get_asset_record(self, asset_project_id: Union[str, ObjectId], asset_name: str):
        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_name": asset_name,
        })

        if record:
            return Asset(**record)
        return None