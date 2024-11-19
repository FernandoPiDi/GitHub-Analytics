import uuid
from datetime import datetime
from typing import Any, Dict

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.base import StructuredTool
from langchain_core.messages import AIMessage
from langchain_experimental.tools import PythonREPLTool

from services.agents.base import BaseAgent
from services.agents.tools import create_developer_output
from services.agents.types import (
    AgentContext,
    AnalystOutput,
    DeveloperOutput,
    PlannerOutput,
)

DEVELOPER_SYSTEM_MESSAGE = """You are a senior TypeScript developer specializing in data visualization.
You are an expert using only the "Recharts" visualization library.

Your task is to:
1. Implement the technical specifications provided by the planner
2. Write clean, maintainable TypeScript code
3. Include proper error handling and type safety
4. Follow best practices for the chosen visualization library
5. Provide clear documentation and comments

Focus on:
- Code quality and readability
- Type safety and error handling
- Responsive design
- Every generated chart should be well labeled and manage dates properly.

The analyst will provide:
- A sample of the data for you to understand the data structure
- The route to retrieve the full dataset in JSON format
- Have in mind that most of the data points have a `label` field. This label field categorizes the data point. 

Output generation:
- You must always invoke the tool **create_developer_output** to return your work.

The current date is: {current_date}

The output code should export the chart component as default and named "Chart".
Use the sample data to understand how to create the visualization.
In the code load the full data from the data.json file path provided by the analyst.
Avoid at all costs using fetching data from external APIs.
My job depends on you, so please do your best."""


class DeveloperAgent(BaseAgent):
    """Agent responsible for implementing the technical specifications."""

    def _create_agent_executor(self) -> AgentExecutor:
        create_developer_output_tool = StructuredTool.from_function(
            name="create_developer_output",
            description="You must use this tool to generate your development output",
            func=create_developer_output,
            args_schema=DeveloperOutput,
            return_direct=True,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).partial(current_date=datetime.now().strftime("%Y-%m-%d"))

        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=[
                create_developer_output_tool,
                PythonREPLTool(),
                *self.tools,
            ],
            prompt=prompt,
            strict=True,
        )

        return AgentExecutor(
            agent=agent,
            tools=[
                create_developer_output_tool,
                PythonREPLTool(),
                *self.tools,
            ],
            verbose=True,
            handle_parsing_errors=True,
        )

    def execute(self, context: Dict[str, Any]) -> AgentContext:
        """Execute the development phase."""
        planner_output = PlannerOutput.model_validate(
            context.get("planner_output", {}) or {}
        )
        analyst_output = AnalystOutput.model_validate(
            context.get("analyst_output", {}) or {}
        )

        result = self.agent_executor.invoke(
            {
                "input": (
                    "Implement the following technical specifications in TypeScript:\n"
                    f"Requirements: {planner_output.requirements}\n"
                    f"Technical Specs: {planner_output.technical_specs}\n"
                    f"Use the following data sample to understand the data structure:\n"
                    f"Data sample: {analyst_output.data_sample}\n"
                    f"Data description: {analyst_output.data_description}\n"
                    f"Load the full data using axios or fetch from the following static route:\n"
                    f"Full Dataset route: {analyst_output.file_route}\n"
                    f"You must always invoke use tool **create_developer_output** to return your work.\n"
                    f"I will a pay 300% tip if you invoke the tool create_developer_output correctly."
                )
            }
        )

        # Parse the result into structured output
        developer_output = DeveloperOutput(
            typescript_code=result["output"]["typescript_code"],
            explanation=result["output"]["explanation"],
            error_message=result["output"].get("error_message", None),
        )

        context.pop("chat_history", None)
        return AgentContext(
            **context,
            chat_history=[
                AIMessage(
                    id=str(uuid.uuid4()),
                    content=developer_output.model_dump_json(),
                    name="developer",
                )
            ],
            developer_output=developer_output,
        )
