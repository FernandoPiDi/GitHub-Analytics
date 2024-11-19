import json
import uuid
from typing import Any, Dict

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.base import StructuredTool
from langchain_core.messages import AIMessage

from services.agents.base import BaseAgent
from services.agents.tools import create_technical_plan
from services.agents.types import (
    AgentContext,
    PlannerOutput,
    TechnicalSpecs,
)

PLANNER_SYSTEM_MESSAGE = """You are a senior software architect responsible for analyzing user requirements and creating detailed technical specifications.

Your task is to analyze chart generation requests and provide a structured output containing:

1. Requirements:
   - List specific functional requirements
   - Include data requirements
   - Define user interaction requirements

2. Acceptance Criteria:
   - List specific, testable criteria
   - Include data validation criteria
   - Define performance expectations

3. Technical Specifications:
   - Chart Type: Specify the exact chart type (line, bar, etc.)
   - Library: Theonly available library to develop the solution is "Recharts"
   - Data Format: Define the exact structure of required data
   - Technical Guidelines: List implementation guidelines and constraints

Be precise and thorough. 
Your output will be parsed into a structured format and used directly for implementation."""


class PlannerAgent(BaseAgent):
    """Agent responsible for planning and requirements analysis."""

    def _create_agent_executor(self) -> AgentExecutor:
        # Create a tool using the Pydantic model
        create_plan_tool = StructuredTool.from_function(
            name="create_technical_plan",
            description="You must use this tool to generate the technical plan",
            func=create_technical_plan,  # Dummy function as we're using it for schema only
            args_schema=PlannerOutput,
            return_direct=True,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=[create_plan_tool, *self.tools],
            prompt=prompt,
            strict=True,
        )

        return AgentExecutor(
            agent=agent,
            tools=[create_plan_tool, *self.tools],
            verbose=True,
            handle_parsing_errors=True,
        )

    def execute(self, context: Dict[str, Any]) -> AgentContext:
        """Execute the planning phase."""
        result = self.agent_executor.invoke(
            {
                "input": (
                    f"Create a technical plan for generating a chart based on this request: {
                        context['message']}\n"
                    f"The chart will visualize data from the GitHub repository: {
                        context['owner']}/{context['repo']}\n\n"
                )
            },
        )

        # Parse the result into a PlannerOutput instance
        plan_data = PlannerOutput(
            requirements=result["output"]["requirements"],
            acceptance_criteria=result["output"]["acceptance_criteria"],
            technical_specs=TechnicalSpecs(
                **json.loads(result["output"]["technical_specs"]),
            ),
            error_message=result["output"].get("error_message", None),
        )

        context.pop("chat_history", None)
        return AgentContext(
            **context,
            chat_history=[
                AIMessage(
                    id=str(uuid.uuid4()),
                    content=plan_data.model_dump_json(),
                    name="planner",
                )
            ],
            planner_output=plan_data,
        )
