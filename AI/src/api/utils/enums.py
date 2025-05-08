from enum import Enum

class IndustryEnum(str, Enum):
    공공 = "공공"
    제조 = "제조"
    금융 = "금융"
    유통물류 = "유통/물류"
    IT통신 = "IT/통신"
    서비스업 = "서비스업"
    기타 = "기타"

class InterestEnum(str, Enum):
    스마트팩토리 = "스마트 팩토리"
    ESG = "ESG"
    고객상담자동화 = "고객 상담 자동화"
    문서자동화 = "문서 자동화"
    AI분석 = "AI 분석"
    업무효율화 = "업무 효율화"

class ReportTypeEnum(str, Enum):
    PDF = "PDF"
    MD = "MD"