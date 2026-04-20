from tavily import TavilyClient
from app.core.config import settings

# Tavily Client initialization
tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

def search_real_reviews(query: str):
    """
    Search depth 'advanced' is used to get high-quality content 
    suitable for LLM analysis.
    """
    try:
        search_result = tavily.search(query=query, search_depth="advanced", max_results=5)
        return search_result['results']
    except Exception as e:
        print(f"Error fetching from Tavily: {e}")
        return []