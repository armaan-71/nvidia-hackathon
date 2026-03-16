import logging
import json
import os
from typing import List, Dict, Any, Optional
from .base import BaseAgent
from tools.web_search import WebSearchTool

logger = logging.getLogger(__name__)

class DiscoveryAgent(BaseAgent):
    """
    Specialist for searching and discovering grant opportunities.
    """
    def __init__(self, config_path: str = "backend/agents/discovery.yaml"):
        # Handle path relative to project root or backend/
        if not os.path.exists(config_path) and os.path.exists("agents/discovery.yaml"):
            config_path = "agents/discovery.yaml"
        super().__init__(config_path)
        self.search_tool = WebSearchTool()

    async def run(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Uses Nemotron for reasoning and Tavily for searching.
        """
        logger.info(f"Discovery Agent processing: {user_input}")
        
        # 1. Ask Nemotron to generate search queries based on user intent
        prompt = f"The user wants to find grants. Extract a highly optimized search query for finding relevant RFPs/grants. User Input: {user_input}"
        
        # Simple reasoning for now: Just get the query
        # In a full ReAct loop, we'd do tool calling, but for the hackathon MVP,
        # we'll use a fast Reason-then-Act pattern.
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a search query optimizer. Return ONLY a single search query string."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        logger.debug(f"NIM raw response: {response}")
        raw_content = response.choices[0].message.content
        
        # Handle cases where NIM returns results in reasoning_content or via dict access
        if raw_content is None:
            # Try dict-like access or model_extra for non-standard fields
            msg_obj = response.choices[0].message
            raw_content = getattr(msg_obj, "reasoning_content", None)
            if raw_content is None and hasattr(msg_obj, "model_extra"):
                raw_content = msg_obj.model_extra.get("reasoning_content")
            
        if raw_content is None:
            logger.error(f"NIM returned None for query optimization. Full response: {response}")
            optimized_query = user_input # Fallback
        else:
            optimized_query = str(raw_content).strip().strip('"')
            
        logger.info(f"Optimized Query: {optimized_query}")

        # 2. Execute search
        search_results = await self.search_tool.search(optimized_query)
        if not search_results:
            return {
                "message": f"I optimized your search to '{optimized_query}' but couldn't find any specific grant results at the moment. Try being more specific with the location or keywords.",
                "data": {"grants": []},
                "active_agent": self.name,
                "suggested_actions": ["Try again", "Enter RFP manually"]
            }
        
        # 3. Summarize results with Nemotron
        summary_prompt = "Based on these search results, summarize the top 3 grant opportunities found. Include specific deadlines and amounts if available. Be concise."
        summary_prompt += f"\n\nResults:\n{json.dumps(search_results[:5])}"
        
        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=self.temperature
        )
        
        final_message = final_response.choices[0].message.content
        
        # Again, check reasoning_content for the final summary if content is None
        if final_message is None:
            msg_obj = final_response.choices[0].message
            final_message = getattr(msg_obj, "reasoning_content", None)
            if final_message is None and hasattr(msg_obj, "model_extra"):
                final_message = msg_obj.model_extra.get("reasoning_content")

        if final_message is None:
            final_message = "I found some results but failed to summarize them. View the raw data below."

        return {
            "message": final_message,
            "data": {"grants": search_results},
            "active_agent": self.name,
            "suggested_actions": self.config.get("suggested_actions", [])
        }
