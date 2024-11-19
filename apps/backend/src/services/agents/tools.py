from typing import Any, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, PrivateAttr

from services.agents.types import (
    Commits,
    GetRepoIssuesInput,
    GetRepoPullRequestsInput,
    Issues,
    PullRequests,
    RepoInput,
    TechnicalSpecs,
)
from services.gql.client import Client
from services.gql.enums import IssueState, PullRequestState, StatusState
from services.gql.get_repo_commits import (
    GetRepoCommitsRepositoryDefaultBranchRefTargetCommit,
)


def create_developer_output(
    typescript_code: str,
    explanation: str,
    error_message: str | None = None,
) -> dict[str, Any]:
    """
    Generate the structured output for the developer agent

    Args:
        typescript_code: The TypeScript code to be returned
        explanation: The explanation of the code
        error_message: The error message if the task cannot be accomplished
    """
    return {
        "typescript_code": typescript_code,
        "explanation": explanation,
        "error_message": error_message,
    }


def create_technical_plan(
    requirements: list[str],
    acceptance_criteria: list[str],
    technical_specs: TechnicalSpecs,
    error_message: str | None = None,
) -> dict[str, Any]:
    """
    Generate the structured output for the technical planner agent

    Args:
        requirements: The requirements for the task
        acceptance_criteria: The acceptance criteria for the task
        technical_specs: The technical specifications for the task
        error_message: The error message if the task cannot be accomplished
    """
    return {
        "requirements": requirements,
        "acceptance_criteria": acceptance_criteria,
        "technical_specs": technical_specs.model_dump_json(),
        "error_message": error_message,
    }


class GetRepoIssuesTools(BaseTool):
    """Tool that gets the latest issues from a GitHub repository."""

    name: str = "get_repo_issues"
    description: str = "Get the latest 100 issues from a GitHub repository"
    args_schema: Type[BaseModel] = GetRepoIssuesInput
    _client: Client = PrivateAttr()

    def __init__(
        self,
        client: Client,
        return_direct: bool = True,
    ):
        super().__init__()
        self._client = client
        self.return_direct = return_direct

    def _run(
        self,
        owner: str,
        name: str,
        states: list[IssueState],
    ) -> list[dict[str, Any]]:
        """Run the tool asynchronously."""
        issue_states = [IssueState(state) for state in states]
        result = self._client.get_repo_issues(
            owner=owner,
            name=name,
            state=issue_states,
        )
        assert result.repository is not None
        assert result.repository.issues is not None
        assert result.repository.issues.edges is not None
        edges = result.repository.issues.edges
        issues: list[dict[str, Any]] = []
        for edge in edges:
            if (not edge) or (not edge.node):
                continue
            labels = []
            if edge.node.labels and edge.node.labels.edges:
                for label in edge.node.labels.edges:
                    if label and label.node:
                        labels.append(label.node.name)
            issues.append(
                Issues(
                    url=edge.node.url,
                    title=edge.node.title,
                    state=edge.node.state,
                    state_reason=edge.node.state_reason,
                    comments_count=edge.node.comments.total_count,
                    created_at=edge.node.created_at,
                    updated_at=edge.node.updated_at,
                    labels=labels,
                ).model_dump(mode="json")
            )
        return issues

    async def _arun(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError("This tool only supports sync execution")


class GetRepoCommitsTool(BaseTool):
    """Tool that gets the latest commits from a GitHub repository."""

    name: str = "get_repo_commits"
    description: str = "Get the latest 100 commits from a GitHub repository"
    args_schema: Type[BaseModel] = RepoInput
    _client: Client = PrivateAttr()

    def __init__(
        self,
        client: Client,
        return_direct: bool = True,
    ):
        super().__init__()
        self._client = client
        self.return_direct = return_direct

    def _run(
        self,
        owner: str,
        name: str,
    ) -> list[dict[str, Any]]:
        """Run the tool asynchronously."""
        result = self._client.get_repo_commits(
            owner=owner,
            name=name,
        )
        assert result.repository is not None
        assert result.repository.default_branch_ref is not None
        assert result.repository.default_branch_ref.target is not None
        assert isinstance(
            result.repository.default_branch_ref.target,
            GetRepoCommitsRepositoryDefaultBranchRefTargetCommit,
        )
        assert result.repository.default_branch_ref.target.history is not None
        assert result.repository.default_branch_ref.target.history.edges is not None
        edges = result.repository.default_branch_ref.target.history.edges
        commits: list[dict[str, Any]] = []
        for edge in edges:
            if not edge or not edge.node:
                continue
            commits.append(
                Commits(
                    message=edge.node.message,
                    author=edge.node.author.name if edge.node.author else None,
                    committed_date=edge.node.committed_date,
                    authored_date=edge.node.authored_date,
                    changed_files_if_available=edge.node.changed_files_if_available
                    if edge.node.changed_files_if_available
                    else 0,
                    additions=edge.node.additions,
                    deletions=edge.node.deletions,
                    status=edge.node.status.state
                    if edge.node.status and edge.node.status.state
                    else StatusState.PENDING,
                ).model_dump(mode="json")
            )
        return commits

    async def _arun(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError("This tool only supports sync execution")


class GetRepoPullRequestsTool(BaseTool):
    """Tool that gets the latest pull requests from a GitHub repository."""

    name: str = "get_repo_pull_requests"
    description: str = "Get the latest 100 pull requests from a GitHub repository"
    args_schema: Type[BaseModel] = GetRepoPullRequestsInput
    _client: Client = PrivateAttr()

    def __init__(
        self,
        client: Client,
        return_direct: bool = True,
    ):
        super().__init__()
        self._client = client
        self.return_direct = return_direct

    def _run(
        self,
        owner: str,
        name: str,
        states: list[PullRequestState],
    ) -> list[dict[str, Any]]:
        """Run the tool asynchronously."""
        pr_states = [PullRequestState(state) for state in states]
        result = self._client.get_repo_pull_requests(
            owner=owner,
            name=name,
            state=pr_states,
        )
        pull_requests: list[dict[str, Any]] = []
        assert result.repository is not None
        assert result.repository.pull_requests is not None
        assert result.repository.pull_requests.nodes is not None
        nodes = result.repository.pull_requests.nodes
        for node in nodes:
            if not node:
                continue
            labels = []
            if node.labels and node.labels.edges:
                for label in node.labels.edges:
                    if label and label.node:
                        labels.append(label.node.name)
            pull_requests.append(
                PullRequests(
                    url=node.url,
                    merged_at=node.merged_at,
                    title=node.title,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                    additions=node.additions,
                    deletions=node.deletions,
                    commits=node.commits.total_count,
                    reviews=node.reviews.total_count if node.reviews else 0,
                    comments=node.comments.total_count if node.comments else 0,
                    state=node.state,
                    labels=labels,
                ).model_dump(mode="json")
            )
        return pull_requests

    async def _arun(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError("This tool only supports sync execution")
