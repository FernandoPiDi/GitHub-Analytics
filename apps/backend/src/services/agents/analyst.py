import json
import uuid
from pathlib import Path
from typing import Any, Dict

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage

from services.agents.base import BaseAgent
from services.agents.types import AgentContext, AnalystOutput, PlannerOutput

ANALYST_SYSTEM_MESSAGE = """You are a data analyst specializing in GitHub repository analytics and data transformation.

Your tools:
1. get_repo_issues: Fetches latest 100 issues with optional state filter
2. get_repo_commits: Fetches latest 100 commits
3. get_repo_pull_requests: Fetches latest 100 PRs with optional state filter

Your task is to:
1. Analyze the planner's requirements to determine needed data
2. Select and use the appropriate GitHub API tools
3. Transform the raw data into a format suitable for charting
4. Provide clear data structure documentation
5. Handle data aggregation and formatting

Focus on:
- Selecting relevant data points
- Proper data transformation
- Time series formatting when needed
- Statistical calculations if required
- Clear data structure documentation

Ensure the data is properly formatted for chart visualization."""


class DataAnalystAgent(BaseAgent):
    """Agent responsible for data analysis and transformation."""

    def _create_agent_executor(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
            strict=True,
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
        )

    def execute(self, context: Dict[str, Any]) -> AgentContext:
        """Execute the data analysis phase."""
        planner_output = PlannerOutput.model_validate(
            context.get("planner_output", {}) or {}
        )

        result = self.agent_executor.invoke(
            {
                "input": (
                    "Analyze the following requirements and fetch appropriate GitHub data:\n"
                    f"Requirements: {planner_output.requirements}\n"
                    f"Technical Specs: {planner_output.technical_specs}\n"
                    f"For repository: {context['owner']}/{context['repo']}\n"
                    "Determine which data to fetch and how to transform it for visualization."
                )
            }
        )

        # Write the data to a file
        parent_dir = f"../frontend/public/charts/{
            context['owner']}/{context['repo']}"
        Path(parent_dir).mkdir(parents=True, exist_ok=True)
        file_path = f"{parent_dir}/data.json"
        with open(file_path, "w") as f:
            json.dump(result["output"], f)

        # Extract or generate data schema description from the output
        sample_item = result["output"][0]
        data_description = {
            "schema": {
                field: type(value).__name__
                for field, value in sample_item.items()
            },
            "total_records": len(result["output"]),
            "sample_fields": list(sample_item.keys())
        }

        analyst_output = AnalystOutput(
            data_sample=result["output"][:10],
            data_description=data_description,
            file_route=f"/charts/{context['owner']
                                  }/{context['repo']}/data.json",
        )

        context.pop("chat_history", None)
        return AgentContext(
            **context,
            chat_history=[
                AIMessage(
                    id=str(uuid.uuid4()),
                    content=analyst_output.model_dump_json(),
                    name="analyst",
                )
            ],
            analyst_output=analyst_output,
        )
