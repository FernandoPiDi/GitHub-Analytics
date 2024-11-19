# Generated by ariadne-codegen
# Source: ./src/queries/

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import IssueState, IssueStateReason


class GetRepoIssues(BaseModel):
    repository: Optional["GetRepoIssuesRepository"]


class GetRepoIssuesRepository(BaseModel):
    issues: "GetRepoIssuesRepositoryIssues"


class GetRepoIssuesRepositoryIssues(BaseModel):
    page_info: "GetRepoIssuesRepositoryIssuesPageInfo" = Field(alias="pageInfo")
    edges: Optional[List[Optional["GetRepoIssuesRepositoryIssuesEdges"]]]


class GetRepoIssuesRepositoryIssuesPageInfo(BaseModel):
    has_next_page: bool = Field(alias="hasNextPage")
    end_cursor: Optional[str] = Field(alias="endCursor")


class GetRepoIssuesRepositoryIssuesEdges(BaseModel):
    node: Optional["GetRepoIssuesRepositoryIssuesEdgesNode"]


class GetRepoIssuesRepositoryIssuesEdgesNode(BaseModel):
    title: str
    url: Any
    state: IssueState
    state_reason: Optional[IssueStateReason] = Field(alias="stateReason")
    created_at: Any = Field(alias="createdAt")
    updated_at: Any = Field(alias="updatedAt")
    comments: "GetRepoIssuesRepositoryIssuesEdgesNodeComments"
    labels: Optional["GetRepoIssuesRepositoryIssuesEdgesNodeLabels"]


class GetRepoIssuesRepositoryIssuesEdgesNodeComments(BaseModel):
    total_count: int = Field(alias="totalCount")


class GetRepoIssuesRepositoryIssuesEdgesNodeLabels(BaseModel):
    edges: Optional[List[Optional["GetRepoIssuesRepositoryIssuesEdgesNodeLabelsEdges"]]]


class GetRepoIssuesRepositoryIssuesEdgesNodeLabelsEdges(BaseModel):
    node: Optional["GetRepoIssuesRepositoryIssuesEdgesNodeLabelsEdgesNode"]


class GetRepoIssuesRepositoryIssuesEdgesNodeLabelsEdgesNode(BaseModel):
    name: str


GetRepoIssues.model_rebuild()
GetRepoIssuesRepository.model_rebuild()
GetRepoIssuesRepositoryIssues.model_rebuild()
GetRepoIssuesRepositoryIssuesEdges.model_rebuild()
GetRepoIssuesRepositoryIssuesEdgesNode.model_rebuild()
GetRepoIssuesRepositoryIssuesEdgesNodeLabels.model_rebuild()
GetRepoIssuesRepositoryIssuesEdgesNodeLabelsEdges.model_rebuild()