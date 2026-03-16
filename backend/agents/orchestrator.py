import logging
import os
from typing import Dict, Any, Optional
from .discovery import DiscoveryAgent
from models import AgentResponse
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    The 'Brain' of Scout. Manages agent sessions and decides 
    which specialist agent should handle the request.
    """
    def __init__(self):
        # Initialize specialists
        self.agents = {
            "discovery": DiscoveryAgent(),
            # "analyzer": AnalyzerAgent(), # Future
            # "scorer": ScorerAgent()      # Future
        }
        
    async def chat(self, user_input: str, session_id: str) -> AgentResponse:
        """
        Main entry point for agentic interactions.
        For now, it defaults to the Discovery Agent.
        In the future, it will use a Router Agent to decide.
        """
        logger.info(f"Orchestrating request for session {session_id}: {user_input}")
        
        # 1. Logic to determine which agent to use
        # Simple heuristic: If it's the start, use discovery.
        selected_agent_name = "discovery"
        
        agent = self.agents.get(selected_agent_name)
        if not agent:
            return AgentResponse(
                message="I'm sorry, I don't have a specialist for that task yet.",
                active_agent="system",
                session_id=session_id
            )

        # 2. Run the specialist
        # Pass context if needed (e.g. state from previous turns)
        result = await agent.run(user_input)
        
        # 3. Format and return
        return AgentResponse(
            message=result["message"],
            active_agent=result["active_agent"],
            session_id=session_id,
            data=result.get("data"),
            suggested_actions=result.get("suggested_actions", []),
            timestamp=datetime.utcnow().isoformat()
        )
