import logging
import os
from typing import Dict, Any, Optional
from .base import BaseAgent
from tools.retrieve_context import RetrieveContextTool

logger = logging.getLogger(__name__)



class AnalyzerAgent(BaseAgent):
    """
    Specialist for analyzing grant eligibility by cross-referencing
    RFP details against the nonprofit's uploaded documents via RAG.
    """
    def __init__(self, config_path: str = "backend/agents/analyzer.yaml"):
        if not os.path.exists(config_path) and os.path.exists("agents/analyzer.yaml"):
            config_path = "agents/analyzer.yaml"
        super().__init__(config_path)
        self.rag_tool = RetrieveContextTool()

    async def run(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes a grant/RFP against the nonprofit's profile using RAG.

        Flow:
        1. Use Nemotron to extract key topics from the user's request.
        2. Retrieve relevant nonprofit documents from ChromaDB.
        3. Ask Nemotron to perform a structured eligibility analysis.
        """
        logger.info(f"Analyzer Agent processing: {user_input}")

        # --- Step 1: Extract key topics for RAG retrieval ---
        topic_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract 2-3 key topics or phrases from this grant description that should be searched in a nonprofit's documents. Return ONLY a comma-separated list of topics."},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )

        topics = self.extract_content(topic_response)
        if not topics:
            topics = user_input
        logger.info(f"Extracted RAG topics: {topics}")

        # --- Step 2: Retrieve nonprofit context from RAG ---
        nonprofit_context = self.rag_tool.retrieve_as_text(topics, n_results=3)
        logger.info(f"RAG context retrieved ({len(nonprofit_context)} chars)")

        # --- Step 3: Perform eligibility analysis ---
        analysis_prompt = f"""Analyze this grant opportunity against our nonprofit's profile.

**Grant/RFP Details:**
{user_input}

**Our Nonprofit's Profile (from uploaded documents):**
{nonprofit_context}

Provide a structured eligibility analysis with:
1. Key eligibility criteria identified from the grant
2. For each criterion: MEETS / PARTIALLY MEETS / DOES NOT MEET with justification
3. Overall eligibility summary
4. Recommended next steps"""

        analysis_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=self.temperature
        )

        analysis_message = self.extract_content(analysis_response)
        if not analysis_message:
            analysis_message = "I retrieved your nonprofit's documents but was unable to generate an analysis. Please try again."

        return {
            "message": analysis_message,
            "data": {
                "topics_searched": topics,
                "nonprofit_context_used": nonprofit_context[:500] + "...",
            },
            "active_agent": self.name,
            "suggested_actions": self.config.get("suggested_actions", [])
        }
