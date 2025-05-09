from langchain_community.tools import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_teddynote.tools.tavily import TavilySearch
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import List, Dict, Annotated
from langchain_teddynote.tools import GoogleNews 
import os

@tool
def search_company(company_name: str) -> str:
    """회사 이름으로 웹 검색 결과 반환 (기업 정보 + 기술 도입 정보)."""

    search_tool = TavilySearchResults(k=5)

    # 첫 번째 쿼리: 일반 기업 정보
    query1 = f"{company_name} 기업 정보"
    results1 = search_tool.invoke({"query": query1})

    # 두 번째 쿼리: 기술 도입 관련 정보
    query2 = f"{company_name} 기술 도입 디지털 전환 AI"
    results2 = search_tool.invoke({"query": query2})

    # 결과 합치기
    combined_snippets = []

    for res in results1:
        combined_snippets.append(f"[일반정보]\n- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}")

    for res in results2:
        combined_snippets.append(f"[기술도입]\n- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}")

    return "\n\n".join(combined_snippets)

@tool
def search_web(input: str) -> str:
    """웹 검색 결과 반환."""
    search_tool = TavilySearchResults(k=5)
    results = search_tool.invoke({"query": f"{input}"})
    snippets = [
        f"- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}"
        for res in results
    ]
    return "\n".join(snippets)

@tool
def extract_keywords(text: str) -> str:
    """주어진 텍스트에서 핵심 키워드 추출."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return llm.invoke(f"다음 텍스트에서 핵심 키워드를 5개 뽑아줘 (콤마로 구분):\n\n{text}")

@tool
def search_news(query: str) -> List[Dict[str, str]]:
    """입력 키워드로 구글 뉴스 검색."""
    news_tool = GoogleNews()
    return news_tool.search_by_keyword(query, k=5)

@tool
def translate_to_english(text: str) -> str:
    """텍스트를 영어로 번역."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return llm.invoke(f"다음 한국어 텍스트를 영어로 번역해줘:\n\n{text}")

def search_docs(query, db):
    results = db.similarity_search(query, k=10)
    return "\n".join([doc.page_content for doc in results])

def load_vector_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "agent_db")
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)