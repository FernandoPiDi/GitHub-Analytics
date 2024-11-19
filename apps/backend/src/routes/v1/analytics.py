"""
Routes for the analytics endpoint.
This endpoint is used to generate charts in typescript
from the repository using Natural Language.
"""

import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from services.agents.analyst import ANALYST_SYSTEM_MESSAGE, DataAnalystAgent
from services.agents.developer import DEVELOPER_SYSTEM_MESSAGE, DeveloperAgent
from services.agents.graph import create_agent_graph
from services.agents.planner import PLANNER_SYSTEM_MESSAGE, PlannerAgent
from services.agents.supervisor import SUPERVISOR_SYSTEM_MESSAGE, SupervisorAgent
from services.agents.tools import (
    GetRepoCommitsTool,
    GetRepoIssuesTools,
    GetRepoPullRequestsTool,
)
from services.gql.client import Client
from utils.config import Settings, get_settings
from validation.api import AnalyticsRequest

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)


async def get_github_client(x_gh_pat: Annotated[str, Header()]) -> Client:
    """Get an authenticated GitHub client."""
    return Client(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {x_gh_pat}"},
    )


@router.post("/")
async def analytics(
    request: AnalyticsRequest,
    client: Annotated[Client, Depends(get_github_client)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    # Initialize the LLMs
    llm = AzureChatOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        model="gpt-4o",
        api_key=settings.azure_openai_api_key.get_secret_value(),  # type: ignore
    )

    llm_mini = AzureChatOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        model="gpt-4o-mini",
        api_key=settings.azure_openai_api_key.get_secret_value(),  # type: ignore
    )

    # Create the Supervisor
    supervisor = SupervisorAgent(
        llm=llm_mini,
        tools=[],
        system_message=SUPERVISOR_SYSTEM_MESSAGE,
        team_members=["planner", "analyst", "developer"],
    )

    # Create the agents
    planner = PlannerAgent(
        llm=llm,
        tools=[],
        system_message=PLANNER_SYSTEM_MESSAGE,
    )

    analyst_tools = [
        GetRepoIssuesTools(client=client),
        GetRepoCommitsTool(client=client),
        GetRepoPullRequestsTool(client=client),
    ]
    analyst = DataAnalystAgent(
        llm=llm,
        tools=analyst_tools,
        system_message=ANALYST_SYSTEM_MESSAGE,
    )

    developer = DeveloperAgent(
        llm=llm,
        tools=[],
        system_message=DEVELOPER_SYSTEM_MESSAGE,
    )

    # Create the graph
    graph = create_agent_graph(supervisor, planner, analyst, developer)

    # Initialize the context
    context = {
        "message": request.message,
        "owner": request.owner,
        "repo": request.repo,
        "chat_history": [
            HumanMessage(
                id=str(uuid.uuid4()),
                content=request.message,
                name="user",
            )
        ],
    }
    # Execute the graph
    final_context = graph.invoke(context)
    # The typescript code is the result of the execution.
    # It needs to be dumped into a file.
    parent_dir = f"../frontend/src/app/charts/{request.owner}/{request.repo}/"
    Path(parent_dir).mkdir(parents=True, exist_ok=True)
    file_path = f"{parent_dir}/chart.tsx"
    with open(file_path, "w") as f:
        f.write(final_context["developer_output"].typescript_code)

    return {
        "typescript_code": final_context["developer_output"].typescript_code,
        "explanation": final_context["developer_output"].explanation,
    }
