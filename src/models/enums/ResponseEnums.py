from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SCCESS="file_validate_successfully"
    File_type_not_supported = "File_type_not_supported"
    File_size_Exceeded = "File_size_Exceeded"
    FILE_UPLOAD_SUCCESS="file_upload_success"
    FILE_UPLOAD_FAILEd= "file_upload_failed"
