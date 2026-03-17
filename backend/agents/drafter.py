import logging
import os
from typing import Dict, Any, Optional
from .base import BaseAgent
from tools.retrieve_context import RetrieveContextTool

logger = logging.getLogger(__name__)


class DrafterAgent(BaseAgent):
    """
    Specialist for drafting grant proposal content by synthesizing
    nonprofit profile data with grant requirements.
    """
    def __init__(self, config_path: str = "backend/agents/drafter.yaml"):
        if not os.path.exists(config_path) and os.path.exists("agents/drafter.yaml"):
            config_path = "agents/drafter.yaml"
        super().__init__(config_path)
        self.rag_tool = RetrieveContextTool()

    async def run(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Drafts a proposal outline or narrative.
        
        user_input should contain grant details or a specific drafting request.
        """
        logger.info(f"Drafter Agent processing request.")

        # --- Step 1: Extract topics for RAG context retrieval ---
        topic_prompt = f"Extract 2-3 key topics from this drafting request to retrieve relevant nonprofit context. Return ONLY a comma-separated list. Request: {user_input}"
        topic_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a context retrieval optimizer."},
                {"role": "user", "content": topic_prompt}
            ],
            temperature=0
        )
        topics = self.extract_content(topic_response) or user_input
        logger.info(f"Drafter RAG topics: {topics}")

        # --- Step 2: Retrieve context ---
        nonprofit_context = self.rag_tool.retrieve_as_text(topics, n_results=3)

        # --- Step 3: Generate Draft ---
        draft_prompt = f"""Generate a grant proposal draft based on the following information.

**Request/Grant Details:**
{user_input}

**Nonprofit Context (from knowledge base):**
{nonprofit_context}

Provide a structured proposal draft including:
1. Executive Summary
2. Organizational Background
3. Statement of Need (tailored to the grant)
4. Program Description
5. Impact & Metrics
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": draft_prompt}
            ],
            temperature=self.temperature
        )

        message = self.extract_content(response)
        if not message:
            message = "I was unable to generate a proposal draft at this time."

        return {
            "message": message,
            "data": {
                "topics_retrieved": topics,
                "context_length": len(nonprofit_context)
            },
            "active_agent": self.name,
            "suggested_actions": self.config.get("suggested_actions", [])
        }
