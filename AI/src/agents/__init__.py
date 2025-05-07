from .ai_adoption import AIAdoptionAgent
from .auto_chat import AutoChatbotAgent
from dotenv import load_dotenv

load_dotenv()

AGENT_REGISTRY = {
    "ai_adoption": AIAdoptionAgent(),
    "auto_chat": AutoChatbotAgent()
}