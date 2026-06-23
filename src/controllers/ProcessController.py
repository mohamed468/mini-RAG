from .BaseController import BaseController
from .ProjectController import ProjectController
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnums

class ProcessController (BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)

    def get_file_extension(self, file_id :str):
        return os.path.splitext(file_id)[-1].lower()


    def get_file_loader(self, file_id: str):
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path, file_id)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_ext == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnums.PDF.value:
            return PyMuPDFLoader (file_path)

        raise ValueError(f"Unsupported file type '.{file_ext}' for file '{file_id}'")

    def get_file_content(self, file_id:str):
        try:
            loader = self.get_file_loader(file_id=file_id)
            documents = loader.load()
            
            # لو الـ loader رجع قائمة فاضية (معناها الملف فاضي)
            if not documents:
                print("DEBUG: Loader returned empty list (Empty File?)")
                return None
                
            return documents
        except Exception as e:
            print(f"DEBUG: Error inside get_file_content: {e}")
            return None

    def process_file_content(self, file_id: str,
                     file_content:list, chunk_size=100, overlap_size= 20 ):
        if not file_content:
            return None

        text_spliter= RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )

        file_content_text= [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata=[
            rec.metadata
            for rec in file_content

        ]

        chunks = text_spliter.create_documents(
            file_content_text,
            metadatas= file_content_metadata
        )

        return chunks












