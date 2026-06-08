from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SCCESS="file_validate_successfully"
    File_type_not_supported = "File_type_not_supported"
    File_size_Exceeded = "File_size_Exceeded"
    FILE_UPLOAD_SUCCESS="file_upload_success"
    FILE_UPLOAD_FAILEd= "file_upload_failed"
    PROCESSING_SUCCESS="processing_success"
    PROCESSING_FAILED="processing_failed"
    FILE_UPLOAD_FAILED ="INVALID_FILE_NAME"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VETORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VETORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrived"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_sucess"