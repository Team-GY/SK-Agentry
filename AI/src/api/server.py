from fastapi import FastAPI
from agents import AGENT_REGISTRY

app = FastAPI()

@app.post("/run_agent/{agent_id}")
def run_agent(agent_id: str, input_data: dict):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        return {"error": f"Agent '{agent_id}' not found."}
    result = agent.run(input_data)
    return {"result": result}