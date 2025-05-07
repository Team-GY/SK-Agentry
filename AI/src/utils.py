from langchain_community.tools import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import os

def search_web(company_name):
    search_tool = TavilySearchResults(k=5)
    results = search_tool.invoke({"query": f"{company_name} 기업 정보"})
    snippets = [
        f"- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}\n  URL: {res.get('url', '')}"
        for res in results
    ]
    return "\n".join(snippets)

def search_docs(query, db):
    results = db.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

def load_vector_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "agent_db")
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)