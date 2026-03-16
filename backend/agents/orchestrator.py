import logging
import os
from typing import Dict, Any, Optional
from .discovery import DiscoveryAgent
from .analyzer import AnalyzerAgent
from .scorer import ScorerAgent
from models import AgentResponse
from datetime import datetime

logger = logging.getLogger(__name__)

# Keywords that indicate the user wants analysis vs discovery
ANALYZER_KEYWORDS = [
    "analyze", "eligibility", "eligible", "qualify", "compare",
    "criteria", "requirement", "deep dive",
    "check", "review", "assess", "evaluate", "rfp"
]

SCORER_KEYWORDS = [
    "score", "match", "rating", "rank", "percent", "percentage", "points"
]

class AgentOrchestrator:
    """
    The 'Brain' of Scout. Manages agent sessions and decides 
    which specialist agent should handle the request.
    """
    def __init__(self):
        # Initialize specialists
        self.agents = {
            "discovery": DiscoveryAgent(),
            "analyzer": AnalyzerAgent(),
            "scorer": ScorerAgent()
        }
        
    def _route(self, user_input: str) -> str:
        """
        Simple intent-based routing.
        Determines which specialist agent should handle the request.
        """
        lower = user_input.lower()
        
        # Priority 1: Scorer
        for keyword in SCORER_KEYWORDS:
            if keyword in lower:
                return "scorer"
                
        # Priority 2: Analyzer
        for keyword in ANALYZER_KEYWORDS:
            if keyword in lower:
                return "analyzer"
        
        return "discovery"

    async def chat(self, user_input: str, session_id: str) -> AgentResponse:
        """
        Main entry point for agentic interactions.
        Routes to the appropriate specialist based on intent detection.
        """
        selected_agent_name = self._route(user_input)
        logger.info(f"Orchestrating [{selected_agent_name}] for session {session_id}: {user_input[:80]}...")
        
        agent = self.agents.get(selected_agent_name)
        if not agent:
            return AgentResponse(
                message="I'm sorry, I don't have a specialist for that task yet.",
                active_agent="system",
                session_id=session_id
            )

        result = await agent.run(user_input)
        
        return AgentResponse(
            message=result["message"],
            active_agent=result["active_agent"],
            session_id=session_id,
            data=result.get("data"),
            suggested_actions=result.get("suggested_actions", []),
            timestamp=datetime.utcnow().isoformat()
        )
