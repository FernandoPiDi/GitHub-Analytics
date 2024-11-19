from typing import Any, Dict

from langchain.agents import AgentExecutor
from langchain_openai import AzureChatOpenAI

from services.agents.types import AgentContext


class BaseAgent:
    """Base class for all agents."""

    def __init__(
        self,
        llm: AzureChatOpenAI,
        tools: list[Any],
        system_message: str,
    ):
        self.llm = llm
        self.tools = tools
        self.system_message = system_message
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """Create the agent executor."""
        raise NotImplementedError(
            "Subclasses must implement _create_agent_executor")

    async def execute(self, context: Dict[str, Any]) -> AgentContext:
        """Execute the agent with the given context."""
        raise NotImplementedError("Subclasses must implement execute")
