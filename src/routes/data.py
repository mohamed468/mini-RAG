from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController, ProjectController , ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes import DataChunk,Asset
from models.enums.AssetTypeEnum import AssetTypeEnum

logger= logging.getLogger('uvicorn.error')   #  في شكل ملف اقدر افحصه واعرف المشكلة فينerrors هيجيب ال 
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

# 👇 شيلنا (file: UploadFile = File(...)) مؤقتاً

@data_router.post("/upload/{project_id}")

async def upload_data(request: Request ,
                      project_id: str, 
                      file: UploadFile = File(...),
                      app_settings : Settings= Depends(get_settings)
                        ):
    print("DEBUG: filename:", file.filename, "content_type:", file.content_type)
    
    # محاولة قراءة أول 64 بايت للتأكد أن الستريم ليس فارغًا
    first = await file.read(64)
    await file.seek(0)    
    # مهم جداً: إرجاع المؤشر للصفر عشان الكود الباقي يقدر يقرأ الملف من الأول

    project_model = await ProjectModel.create_instance(
        db_client= request.app.db_client #pro_id عشان اقدر استدعيه واديله ال project model كده حصلت على ال 
    )
    project = await project_model.get_project_or_create_one(
        project_id= project_id               # project idال جواه وخليتها تاخد ال funكده استعديته وناديت ال 
    )
    # 1. التحقق من وجود اسم للملف (تعديل الأمان)
    if not file.filename:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            # تأكد إنك ضفت INVALID_FILE_NAME في الـ Enum أو استخدم رسالة نصية مؤقتاً
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value} 
        )
    # Validate the file properites
    data_controller = DataController()
    is_valid, result_Signal = data_controller.validate_uploaded_file(file= file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content= {
                "signal" : result_Signal
            }
        )
    project_dir_path= ProjectController().get_project_path(project_id=project_id)
    file_path, file_id= data_controller.generate_unique_filepath(
        orig_file_name= file.filename,
        project_id= project_id
    )

    try:         
        await file.seek(0)

       # ب) تحديد حجم الـ Chunk (من الكونفيج، ولو بايظ نستخدم 1 ميجا احتياطي)
        chunk_size = app_settings.FILE_DEFAULT_CHUNK_SIZE
        if not chunk_size or chunk_size <= 0:
            chunk_size = 1024 * 1024  # 1MB Fallback
            
        # ج) الكتابة مع عداد (عشان نتأكد إنه متكتبش فاضي)
        total_bytes_written = 0
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await f.write(chunk)
                total_bytes_written += len(chunk)
        
        # د) لو العداد صفر، يبقى فيه مشكلة، نمسح الملف ونبلغ المستخدم
        if total_bytes_written == 0:
            logger.error("Uploaded file is empty (0 bytes written).")
            if os.path.exists(file_path):
                os.remove(file_path)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value, "error": "File is empty"}
            )

    except Exception as e:
        logger.error(f"Error While Uploading File: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )
    #Store the assets into the database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    assert project.id is not None
    
    asset_resource = Asset(
        asset_project_id= project.id,
        asset_type= AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)


    
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": str(asset_record.id),
        }
    )            

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    #get pro or create ب project واجيب ال projrctmodelمن الداتابيزمن خلال تعريف project_idمحتاج اجيب ال 

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    if not project.id:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value,
                "error": "Project ID is missing from database record"
            }
        )

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    project_files_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_ID_ERROR.value,
                }
            )

        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }

    else:
        project_files = await asset_model.get_all_project_assets(
            asset_project_id = project.id,
            asset_type=AssetTypeEnum.FILE.value,
        )

        project_files_ids = {
            record.id: record.asset_name
            for record in project_files
        }

    # 👇 ده لازم يكون بره الـ if/else عشان يتشيك في الحالتين
    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_ERROR.value,
            }
        )

    process_controller = ProcessController(project_id=project_id)
    no_records = 0
    no_files = 0

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if do_reset == 1:
        #await بيعبر ان في هنا متغير ولكن أنا معنديش أهتمام بعرض أنا بس كتبته كده عشان ال  under score هنا ال 
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    for asset_id, file_id in project_files_ids.items():
        if asset_id is None:
            logger.error(f"Asset ID is None for file: {file_id}")
            continue
        file_content = process_controller.get_file_content(file_id=file_id)

        if not file_content:
            logger.error(f"Error while processing file: {file_id}")
            continue   # 👈 المدرس قال نكمل ولا نوقف، فاستخدم continue بدل return

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )

        if not file_chunks:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROCESSING_FAILED.value
                }
            )

        #Datachunk بتاع object الى filechunk هنا عايز احول 
        # return file_chunks

        file_chunks_records = [
            #وأحط القيم بتاعتهاDatachunkهنا هجيب محتويات ال 
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            
            for i, chunk in enumerate(file_chunks)
        ]
        # recordsكده بقى معايا ال 
            #بتاعهorderهترجعه هترجع ال elementولكن مع كل file chunksدي هترجع enumerateهنا 
        # projrctmodelزي ما عرفنا ال chunkmodelهعرف ال 

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )