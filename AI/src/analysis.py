from tools import search_web, search_docs
from prompts import summary_chain
import os
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

def analyze_company(company_name, vector_db, user_data):
    # 1. 외부 검색 + 요약
    web_context = search_web(company_name)
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', streaming=True)
    chain = load_summarize_chain(llm, chain_type="stuff")
    docs = [Document(page_content=web_context)]
    query = chain.run(docs)

    # 2. 내부 문서 검색
    pdf_context = search_docs(query, vector_db)

    # 3. 날짜 포맷 변환
    created_date = user_data["created_date"].strftime("%Y년 %m월 %d일")

    # 4. summary_chain 입력값 구성
    summary_input = {
        "company_name": company_name,
        "web_context": web_context,
        "pdf_context": pdf_context,
        "industry": user_data["industry"],
        "scale": user_data["scale"],
        "interests": user_data["interests"],
        "budget_size": user_data["budget_size"],
        "created_date": created_date,
    }

    # 5. 요약 리포트 실행
    summary_report = summary_chain.run(summary_input)

    # 6. 경로 설정 및 저장
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(base_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    filename = os.path.join(outputs_dir, f"{company_name}_report.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_report)

    print(f"✅ {filename} 저장 완료!")

    return {
        "summary_report_file": filename
    }
