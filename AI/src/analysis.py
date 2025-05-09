from datetime import datetime
from tools import search_company, search_docs
from prompts import summary_chain, recommend_chain
import os
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document

def json_to_markdown_table(json_data):
    header = "| 에이전트명 | 적용 부서 | 적용 사례 | 연간 절감 시간 | 도입 난이도 |\n"
    header += "|------------|------------|------------|----------------|--------------|\n"
    rows = ""
    for item in json_data:
        rows += f"| {item['에이전트명']} | {item['적용 부서']} | {item['적용 사례']} | {item['연간 절감 시간']} | {item['도입 난이도']} |\n"
    return header + rows

def analyze_company(company_name, vector_db, user_data):
    # 1. 외부 검색 + 요약
    web_context = search_company(company_name)
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', streaming=True)
    chain = load_summarize_chain(llm, chain_type="stuff")
    docs = [Document(page_content=web_context)]
    query = chain.run(docs)

    # 2. 내부 문서 검색
    pdf_context = search_docs(query, vector_db)

    # 추천 chain 실행
    recommended_agents = recommend_chain.run({
        "company_name": company_name,
        "web_context": web_context,
        "pdf_context": pdf_context
    })

    # JSON → Markdown 변환
    recommendation_table = json_to_markdown_table(recommended_agents)

    # 3. 날짜 포맷 변환
    created_date = (user_data.get("created_date") or datetime.today()).strftime("%Y년 %m월 %d일")

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
        "recommendation_table": recommendation_table
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
        "summary_report_file": filename,
        "recommended_agents": recommended_agents
    }
