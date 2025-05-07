from utils import search_web, search_docs
from prompts import recommend_chain, summary_chain, recommend_parser
import os

def analyze_company(company_name, db):
    web_context = search_web(company_name)
    query = f"{company_name} {web_context}"
    pdf_context = search_docs(query, db)

    # Agent 추천
    recommended_agents = recommend_chain.run({
        "company_name": company_name,
        "web_context": web_context,
        "pdf_context": pdf_context,
        "format_instructions": recommend_parser.get_format_instructions()
    })

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
        "recommended_agents": recommended_agents,
        "summary_report_file": filename
    }