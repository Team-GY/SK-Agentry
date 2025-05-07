from agents import AGENT_REGISTRY

agent = AGENT_REGISTRY["ai_adoption"]

input_data = {
    "company_name": "디자이노블",
    "investment_amount": 500,
    "ai_goal": "생산성 향상"
}

result = agent.run(input_data)
print(result)