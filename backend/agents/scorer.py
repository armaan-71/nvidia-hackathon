import logging
import os
from typing import Dict, Any, Optional
from .base import BaseAgent

logger = logging.getLogger(__name__)

def _extract_content(response) -> Optional[str]:
    """
    Extracts text content from a NIM response, checking both
    standard 'content' and Nemotron-specific 'reasoning_content'.
    """
    msg = response.choices[0].message
    content = msg.content
    if content is None:
        content = getattr(msg, "reasoning_content", None)
        if content is None and hasattr(msg, "model_extra"):
            content = msg.model_extra.get("reasoning_content")
    return str(content) if content else None

class ScorerAgent(BaseAgent):
    """
    Specialist for calculating a numeric match score and providing
    a justification based on the eligibility analysis.
    """
    def __init__(self, config_path: str = "backend/agents/scorer.yaml"):
        if not os.path.exists(config_path) and os.path.exists("agents/scorer.yaml"):
            config_path = "agents/scorer.yaml"
        super().__init__(config_path)

    async def run(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates a match score based on analysis.
        
        The user_input should ideally be the output of the Analyzer Agent,
        or a request to score a specific grant analysis.
        """
        logger.info(f"Scorer Agent processing request.")

        # If user input doesn't look like an analysis, we might need to ask for one,
        # but the orchestrator should handle transitions.
        # For now, we assume the input IS the analysis or contains it.

        prompt = f"""Based on the following eligibility analysis, calculate a Match Score (0-100) and provide a justification.

**Eligibility Analysis:**
{user_input}

Return your response in this format:
- **Match Score:** [0-100]
- **Category Breakdown:**
  - Geographic Fit: [0-10]
  - Mission Alignment: [0-10]
  - Capacity: [0-10]
- **Justification:** [Brief summary]
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )

        message = _extract_content(response)
        if not message:
            message = "I was unable to calculate a score based on the provided analysis."

        # Attempt to extract the numeric score for the 'data' field
        score = 0
        try:
            # Very simple parser for "[0-100]"
            if "Match Score:**" in message:
                score_str = message.split("Match Score:**")[1].split("\n")[0].strip()
                # Clean up non-digits
                score_digits = "".join(filter(str.isdigit, score_str))
                score = int(score_digits) if score_digits else 0
        except Exception as e:
            logger.warning(f"Failed to parse numeric score from message: {e}")

        return {
            "message": message,
            "data": {
                "match_score": score,
                "scored_at": os.environ.get("TIMESTAMP", "")
            },
            "active_agent": self.name,
            "suggested_actions": self.config.get("suggested_actions", [])
        }
