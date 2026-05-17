from enum import Enum
class LLEnums(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GEMINI = "GEMINI"
class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    
class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"
    
class GeminiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "model"
class DocumnetTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"

