from tools import search_web, search_docs
from prompts import summary_chain
import os
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

def analyze_company(company_name, vector_db):
    web_context = search_web(company_name)
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', streaming=True)
    chain = load_summarize_chain(llm, chain_type="stuff")
    docs = [Document(page_content=web_context)]
    query = chain.run(docs)
    pdf_context = search_docs(query, vector_db)

    # 요약 리포트
    summary_report = summary_chain.run({
        "company_name": company_name,
        "web_context": web_context,
        "pdf_context": pdf_context
    })

    # src 폴더의 상위 (AI 폴더) 경로 구하기
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(base_dir, "outputs")

    # outputs 폴더가 없다면 생성
    os.makedirs(outputs_dir, exist_ok=True)

    # 파일 경로 설정
    filename = os.path.join(outputs_dir, f"{company_name}_report.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_report)

    print(f"✅ {filename} 저장 완료!")

    return {
        "summary_report_file": filename
    }