import operator
from datetime import datetime
from typing import Annotated, Any, List, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from services.gql.enums import IssueState, PullRequestState, StatusState


class Issues(BaseModel):
    """
    Model to create a dataframe from the issues data.
    """

    url: str
    title: str
    state: IssueState
    state_reason: str | None
    comments_count: int
    created_at: datetime
    updated_at: datetime
    labels: list[str]


class Commits(BaseModel):
    """Model to create a dataframe from the commits data."""

    committed_date: datetime
    authored_date: datetime
    author: str | None
    message: str
    changed_files_if_available: int
    additions: int
    deletions: int
    status: StatusState


class PullRequests(BaseModel):
    """Model to create a dataframe from the pull requests data."""

    url: str
    merged_at: datetime | None
    title: str
    created_at: datetime
    updated_at: datetime
    additions: int
    deletions: int
    commits: int
    reviews: int
    comments: int
    state: PullRequestState
    labels: list[str]


class TechnicalSpecs(BaseModel):
    chart_type: str = Field(description="The type of chart to be generated")
    data_format: str = Field(
        description="Format of the data required for the chart")
    technical_constraints: List[str] = Field(
        description="List of technical constraints"
    )


class PlannerOutput(BaseModel):
    """Output from the planner agent."""

    requirements: List[str] = Field(
        description="List of functional requirements")
    acceptance_criteria: List[str] = Field(
        description="List of acceptance criteria")
    technical_specs: TechnicalSpecs = Field(
        description="Technical specifications for the implementation"
    )
    error_message: str | None = Field(
        description="If you consider that the task cannot be accomplished due to limitations, "
        "please provide a detailed explanation of the limitations and the reasons why the task cannot be accomplished.",
    )


class AnalystOutput(BaseModel):
    """Output from the data analyst agent."""

    data_sample: list[dict[str, Any]] = Field(
        description="A sample of the data to understand the data structure"
    )
    data_description: dict[str, Any] = Field(
        description="A description of the data to understand the data structure"
    )
    file_route: str = Field(
        description="The static route to retrieve the full dataset in JSON format"
    )


class DeveloperOutput(BaseModel):
    """Output from the developer agent."""

    typescript_code: str = Field(description="The typescript code")
    explanation: str | None = Field(description="The explanation for the code")
    error_message: str | None = Field(
        description="If you consider that the task cannot be accomplished due to limitations, "
        "please provide a detailed explanation of the limitations and the reasons why the task cannot be accomplished.",
    )


class AgentContext(TypedDict):
    """Context passed between agents."""

    message: str
    owner: str
    repo: str
    chat_history: Annotated[Sequence[BaseMessage], operator.add]
    next: str | None
    planner_output: PlannerOutput | None
    analyst_output: AnalystOutput | None
    developer_output: DeveloperOutput | None
    error_message: str | None


class RepoInput(BaseModel):
    """Input for repository-related tools."""

    owner: str = Field(description="The owner of the repository")
    name: str = Field(description="The name of the repository")


class GetRepoIssuesInput(RepoInput):
    """Input for get_repo_issues tool."""

    states: list[IssueState] = Field(
        description=(
            "Filter issues by state (OPEN, CLOSED). "
            "If not provided, returns all issues."
        ),
    )


class GetRepoPullRequestsInput(RepoInput):
    """Input for get_repo_pull_requests tool."""

    states: list[PullRequestState] = Field(
        description=(
            "Filter pull requests by state (OPEN, CLOSED, MERGED). "
            "If not provided, returns all PRs."
        ),
    )
