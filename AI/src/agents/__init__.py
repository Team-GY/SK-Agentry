from .ai_adoption import AIAdoptionAgent
from .auto_chat import AutoChatbotAgent
from .weekly_news import WeeklyNewsAgent
from tools import search_news, search_docs, search_web, extract_keywords,search_company
from dotenv import load_dotenv

load_dotenv()

AGENT_REGISTRY = {
    "ai_adoption": AIAdoptionAgent(),
    "auto_chat": AutoChatbotAgent(),
    "weekly_news": WeeklyNewsAgent()
}

TOOL_REGISTRY = {
    "search_weekly": search_news,
    "extract_keywords": extract_keywords,
    "search_docs": search_docs,
    "search_web": search_web,
    "search_company": search_company,
}
