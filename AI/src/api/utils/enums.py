from enum import Enum

class IndustryEnum(str, Enum):
    제조 = "제조"
    금융 = "금융"
    헬스케어 = "헬스케어"

class InterestEnum(str, Enum):
    RAG = "RAG"
    LLM = "LLM"
    AutoML = "AutoML"

class VisibilityEnum(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
