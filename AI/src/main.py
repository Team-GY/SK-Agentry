# main.py
from analysis import analyze_company
from utils import load_vector_db
import json
from dotenv import load_dotenv

def main():
    load_dotenv()
    db = load_vector_db()
    company_name = "sk하이닉스"
    result = analyze_company(company_name, db)

    print("\n=== 추천된 AI Agent ===")
    print(json.dumps(result["recommended_agents"], indent=2, ensure_ascii=False))
    print(f"\n✅ 리포트 파일: {result['summary_report_file']}")

if __name__ == "__main__":
    main()