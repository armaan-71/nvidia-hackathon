import httpx
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from config import get_settings

logger = logging.getLogger(__name__)

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query to find grants or RFP details.")
    max_results: int = Field(5, description="Maximum number of search results to return.")

class WebSearchTool:
    """
    Tool for agents to search the web using the Tavily API.
    Recommended for NVIDIA Nemotron agents.
    """
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.tavily_api_key
        key_show = f"{self.api_key[:4]}..." if self.api_key else "MISSING"
        logger.info(f"WebSearchTool initialized with API Key: {key_show}")
        self.base_url = "https://api.tavily.com/search"

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a search query and returns clean, LLM-ready results.
        """
        if not self.api_key or self.api_key == "your_tavily_api_key_here":
            logger.warning("Tavily API key is missing. Web search will not return results.")
            return []

        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results
        }

        try:
            logger.info(f"Tavily searching for: {query}")
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, json=payload, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                raw_results = data.get("results", [])
                logger.info(f"Tavily found {len(raw_results)} results.")
                
                results = []
                for result in raw_results:
                    results.append({
                        "title": result.get("title"),
                        "url": result.get("url"),
                        "content": result.get("content"),
                        "score": result.get("score")
                    })
                return results
        except httpx.HTTPStatusError as e:
            logger.error(f"Tavily search HTTP error: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return []

# Example usage/test
if __name__ == "__main__":
    import asyncio
    async def main():
        tool = WebSearchTool()
        results = await tool.search("Newest environmental grants for nonprofits 2024")
        print(results)
    
    # asyncio.run(main())
