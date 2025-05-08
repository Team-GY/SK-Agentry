from langchain_community.tools import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import List, Dict, Annotated
from langchain_teddynote.tools import GoogleNews 
import os

@tool
def search_web(company_name: str) -> str:
    """회사 이름으로 웹 검색 결과 반환."""
    from langchain_community.tools import TavilySearchResults
    search_tool = TavilySearchResults(k=5)
    results = search_tool.invoke({"query": f"{company_name} 기업 정보"})
    snippets = [
        f"- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}\n  URL: {res.get('url', '')}"
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