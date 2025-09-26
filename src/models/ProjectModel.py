from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnums import DataBaseEnum
import math


class ProjectModel(BaseDataModel):

    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection= self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):#use model_dump() in pydantic v2 instead dict in v1 
        result = await self.collection.insert_one(project.dict(by_alias = True, exclude_unset= True)) #  وخليته يضيف فالداتابيزdictهنا حولته ل
# لأن من غيرهامش هيتم استخلاص للداتا وهيسبب أيرور. awaitعشان اعرف اعمل async دي تكون fun لأزم ال 

        project._id =result.inserted_id # projectال تمت اضافته على ال id هيرجع ال 
        return project #   idويرجعلي نسخة منه جديدة بال project يعنى هنا هياخد من ال 
    
    # make def to get the project_id or create one if not created

    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id" : project_id
        })

        if record is None :
            #create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)
            return project
        
        return Project(**record) #  بقوله رجعهNone فيه قيمة مش ب record هنا لو خلاص كان ال 
    #  dictوحولت البروجكت ليه فهعمل في النهاية العكس وهو اني احول ال dictبتاخد insert one هنا زي ما كان ال 
    # project modelالي 

    async def get_all_projects(self, page: int=1, page_size:int =10):
        #count total numbers of documents
        total_documents = await self.collection.count_documents({})
        # ({})هنا هخليه يعد كل الملفات ال معايا وده معناه ان مفيش فلتر ف عد كل حاجة وهاتها

        #calculate total number of pages
        # total_pages = math.ceil(total_documents / page_size) 
        # or
        total_pages = total_documents // page_size
        if total_documents % total_pages > 0:
            total_pages += 1


        cursor = self.collection.find().skip((page-1) * page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(
                Project(**document) # project model خليت ال يرجع  
            )

        return projects, total_pages   #برجع اجمالي عدد الصفحات عشان اعرف هفضل ماشي لحد فين
     