from typing import Any

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSerializable
from langchain_openai import AzureChatOpenAI

SUPERVISOR_SYSTEM_MESSAGE = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {team_members}. Given the following user request,"
    " respond with the worker to act next. Ideally the order of execution"
    " should be: planner, analyst, developer. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)


class SupervisorAgent:
    """Agent responsible for managing the team and task allocation."""

    def __init__(
        self,
        llm: AzureChatOpenAI,
        tools: list[Any],
        system_message: str,
        team_members: list[str],
    ):
        self.llm = llm
        self.tools = tools
        self.system_message = system_message
        self.team_members = team_members
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self,) -> RunnableSerializable:

        options = self.team_members.copy()
        options.insert(0, "FINISH")
        next_function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": self.team_members},
                        ],
                    },
                    "error_message": {
                        "title": "Error",
                        "type": "string",
                    },
                },
                "required": ["next"],
            },
        }

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SUPERVISOR_SYSTEM_MESSAGE),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}"
                    "In case the request is unprocessable FINISH and provide"
                    " an error message.",
                ),
            ]
        ).partial(options=str(options), team_members=", ".join(self.team_members))

        return (
            prompt
            | self.llm.bind_functions(
                functions=[next_function_def],
                function_call="route",
            )
            | JsonOutputFunctionsParser()
        )
