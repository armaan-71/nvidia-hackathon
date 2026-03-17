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

# Keywords that indicate intent
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

# Pipeline definitions: which agent flows naturally into which
PIPELINES = {
    "discovery": ["analyzer", "scorer"],     # Discovery -> Analyze -> Score
    "analyzer": ["scorer"],                  # Analyze -> Score
    "scorer": [],                            # Scorer is a terminal step
    "drafter": [],                           # Drafter is a terminal step
}


class AgentOrchestrator:
    """
    The 'Brain' of Scout. Manages agent sessions and decides
    which specialist agent should handle the request.
    Supports multi-agent pipelines where agents chain automatically.
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
        Main entry point. Routes to the starting agent and then
        automatically chains through the pipeline, collecting results.
        """
        start_agent = self._route(user_input)
        logger.info(f"Pipeline start [{start_agent}] for session {session_id}")

        # Save user message
        session_store.append_message(session_id, "user", user_input)

        # Run the pipeline
        pipeline_results = await self._run_pipeline(
            start_agent, user_input, session_id
        )

        # Build the combined response from all pipeline steps
        combined_response = self._build_combined_response(
            pipeline_results, session_id
        )

        # Save assistant message
        session_store.append_message(
            session_id, "assistant",
            combined_response.message,
            agent=combined_response.active_agent
        )

        return combined_response

    async def _run_pipeline(
        self, start_agent: str, user_input: str, session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Runs agents sequentially through the pipeline.
        Each agent's output feeds into the next as context.
        """
        results = []
        current_agent_name = start_agent
        current_input = user_input

        while current_agent_name:
            agent = self.agents.get(current_agent_name)
            if not agent:
                break

            logger.info(f"  ▶ Running [{current_agent_name}]...")
            result = await agent.run(current_input)
            result["_agent_name"] = current_agent_name
            results.append(result)

            # Store the result in the shared workspace
            session_store.set_workspace(
                session_id,
                f"{current_agent_name}_result",
                result.get("message", "")
            )

            # If the agent returned data, store it too
            if result.get("data"):
                session_store.set_workspace(
                    session_id,
                    f"{current_agent_name}_data",
                    result["data"]
                )

            # Determine next agent in the pipeline
            next_agents = PIPELINES.get(current_agent_name, [])
            if next_agents:
                current_agent_name = next_agents[0]
                # Feed the previous agent's output as context for the next
                current_input = result.get("message", user_input)
                logger.info(f"  ⮕ Chaining to [{current_agent_name}]")
            else:
                current_agent_name = None  # End of pipeline

        return results

    def _build_combined_response(
        self, results: List[Dict[str, Any]], session_id: str
    ) -> AgentResponse:
        """
        Merges pipeline results into a single AgentResponse for the frontend.
        Shows a summary of what each agent did.
        """
        if not results:
            return AgentResponse(
                message="I'm sorry, I couldn't process that request.",
                active_agent="system",
                session_id=session_id
            )

        # If only one agent ran, return its result directly
        if len(results) == 1:
            r = results[0]
            return AgentResponse(
                message=r["message"],
                active_agent=r.get("active_agent", r.get("_agent_name", "system")),
                session_id=session_id,
                data=r.get("data"),
                suggested_actions=r.get("suggested_actions", []),
                timestamp=datetime.utcnow().isoformat()
            )

        # Multiple agents ran — build a combined narrative
        sections = []
        combined_data = {}
        last_agent = results[-1].get("_agent_name", "system")

        for r in results:
            agent_name = r.get("_agent_name", "agent")
            label = agent_name.capitalize()
            sections.append(f"### 🔹 {label} Agent\n{r['message']}")

            # Merge data from all agents
            if r.get("data"):
                combined_data[agent_name] = r["data"]

        combined_message = (
            "## Scout Pipeline Report\n\n"
            + "\n\n---\n\n".join(sections)
        )

        # Use the last agent's suggested_actions
        last_actions = results[-1].get("suggested_actions", [])

        return AgentResponse(
            message=combined_message,
            active_agent=last_agent,
            session_id=session_id,
            data=combined_data if combined_data else None,
            suggested_actions=last_actions,
            timestamp=datetime.utcnow().isoformat()
        )
