import logging
import os
from typing import Dict, Any, Optional, List
from .discovery import DiscoveryAgent
from .analyzer import AnalyzerAgent
from .scorer import ScorerAgent
from .drafter import DrafterAgent
from models import AgentResponse
from datetime import datetime
import session_store

logger = logging.getLogger(__name__)

PROFILE_KEYWORDS = [
    "who am i", "my mission", "my organization", "my profile",
    "about me", "about us", "our mission", "tell me about",
    "what do we do", "what is my", "what are my"
]

ANALYZER_KEYWORDS = [
    "analyze", "eligibility", "eligible", "qualify", "compare",
    "criteria", "requirement", "deep dive",
    "check", "review", "assess", "evaluate", "rfp"
]

SCORER_KEYWORDS = [
    "score", "match", "rating", "rank", "percent", "percentage", "points"
]

DRAFTER_KEYWORDS = [
    "draft", "write", "proposal", "narrative", "outline", "apply", "application"
]

# Next Step mapping for the Interactive Workflow
# (Defines the "Suggested Action" text for the next agent)
NEXT_STEPS = {
    "discovery": "Analyze eligibility for these grants",
    "analyzer": "Calculate match scores",
    "scorer": "Draft a proposal for the top match",
    "drafter": None
}


class AgentOrchestrator:
    """
    The 'Brain' of Scout. Manages agent sessions and decides
    which specialist agent should handle the request.
    Supports interactive workflows with manual handoffs.
    """
    def __init__(self):
        self.agents = {
            "discovery": DiscoveryAgent(),
            "analyzer": AnalyzerAgent(),
            "scorer": ScorerAgent(),
            "drafter": DrafterAgent()
        }

    def _route(self, user_input: str) -> str:
        """Simple intent-based routing."""
        lower = user_input.lower()

        # Profile/identity queries → Analyzer (uses RAG)
        for keyword in PROFILE_KEYWORDS:
            if keyword in lower:
                return "analyzer"

        # Check for specific "Next Step" commands first
        if "analyze" in lower and ("eligibility" in lower or "grant" in lower):
            return "analyzer"
        if "score" in lower or "match score" in lower:
            return "scorer"
        if "draft" in lower or "proposal" in lower:
            return "drafter"

        # Fallback to keyword routing
        for keyword in DRAFTER_KEYWORDS:
            if keyword in lower:
                return "drafter"

        for keyword in SCORER_KEYWORDS:
            if keyword in lower:
                return "scorer"

        for keyword in ANALYZER_KEYWORDS:
            if keyword in lower:
                return "analyzer"

        return "discovery"

    async def chat(self, user_input: str, session_id: str) -> AgentResponse:
        """
        Main entry point. Routes to a single agent and provides
        the next step as a suggested action.
        """
        agent_name = self._route(user_input)
        logger.info(f"Interactive Step: [{agent_name}] for session {session_id}")

        # Save user message
        session_store.append_message(session_id, "user", user_input)

        # 1. Prepare input context for the agent
        # If the user is asking for analysis/scoring/drafting, 
        # we might need to pull the previous agent's results from the workspace.
        context_input = self._build_context_input(agent_name, user_input, session_id)

        # 2. Run the single agent
        agent = self.agents.get(agent_name)
        if not agent:
            return AgentResponse(
                message="Agent not found.",
                active_agent="system",
                session_id=session_id
            )

        result = await agent.run(context_input)
        
        # 3. Save results to workspace
        session_store.set_workspace(session_id, f"{agent_name}_result", result.get("message", ""))
        if result.get("data"):
            session_store.set_workspace(session_id, f"{agent_name}_data", result["data"])

        # 4. Determine Suggested Action for the "Next Handoff"
        suggested_actions = result.get("suggested_actions", [])
        next_step_label = NEXT_STEPS.get(agent_name)
        if next_step_label and next_step_label not in suggested_actions:
            suggested_actions.insert(0, next_step_label)

        # Build response
        response = AgentResponse(
            message=result["message"],
            active_agent=agent_name,
            session_id=session_id,
            data=result.get("data"),
            suggested_actions=suggested_actions,
            timestamp=datetime.utcnow().isoformat()
        )

        # Save assistant message
        session_store.append_message(
            session_id, "assistant",
            response.message,
            agent=response.active_agent
        )

        return response

    def _build_context_input(self, agent_name: str, user_input: str, session_id: str) -> str:
        """
        Enriches the user input with previous agent results if needed.
        """
        if agent_name == "analyzer":
            # Analyzer needs Discovery results
            discovery_data = session_store.get_workspace(session_id, "discovery_result")
            if discovery_data:
                return f"Analyze the eligibility of these grants for me: {discovery_data}\nUser additional context: {user_input}"
        
        if agent_name == "scorer":
            # Scorer needs Analyzer results
            analyzer_data = session_store.get_workspace(session_id, "analyzer_result")
            if analyzer_data:
                return f"Provide match scores for this analysis: {analyzer_data}\nUser additional context: {user_input}"

        if agent_name == "drafter":
            # Drafter needs Scorer/Analyzer results
            best_grant = session_store.get_workspace(session_id, "scorer_result") or \
                         session_store.get_workspace(session_id, "analyzer_result")
            if best_grant:
                return f"Draft a proposal for this grant: {best_grant}\nUser additional context: {user_input}"

        return user_input
