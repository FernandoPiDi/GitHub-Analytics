# Generated by ariadne-codegen
# Source: ./src/queries/

from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel
from .enums import StatusState


class GetRepoCommits(BaseModel):
    repository: Optional["GetRepoCommitsRepository"]


class GetRepoCommitsRepository(BaseModel):
    default_branch_ref: Optional["GetRepoCommitsRepositoryDefaultBranchRef"] = Field(
        alias="defaultBranchRef"
    )


class GetRepoCommitsRepositoryDefaultBranchRef(BaseModel):
    target: Optional[
        Annotated[
            Union[
                "GetRepoCommitsRepositoryDefaultBranchRefTargetGitObject",
                "GetRepoCommitsRepositoryDefaultBranchRefTargetCommit",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetRepoCommitsRepositoryDefaultBranchRefTargetGitObject(BaseModel):
    typename__: Literal["Blob", "GitObject", "Tag", "Tree"] = Field(alias="__typename")


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommit(BaseModel):
    typename__: Literal["Commit"] = Field(alias="__typename")
    history: "GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistory"


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistory(BaseModel):
    edges: Optional[
        List[
            Optional["GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdges"]
        ]
    ]


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdges(BaseModel):
    node: Optional[
        "GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNode"
    ]


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNode(BaseModel):
    committed_date: Any = Field(alias="committedDate")
    authored_date: Any = Field(alias="authoredDate")
    author: Optional[
        "GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeAuthor"
    ]
    message: str
    committer: Optional[
        "GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeCommitter"
    ]
    changed_files_if_available: Optional[int] = Field(alias="changedFilesIfAvailable")
    additions: int
    deletions: int
    status: Optional[
        "GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeStatus"
    ]


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeAuthor(
    BaseModel
):
    name: Optional[str]


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeCommitter(
    BaseModel
):
    name: Optional[str]


class GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNodeStatus(
    BaseModel
):
    state: StatusState


GetRepoCommits.model_rebuild()
GetRepoCommitsRepository.model_rebuild()
GetRepoCommitsRepositoryDefaultBranchRef.model_rebuild()
GetRepoCommitsRepositoryDefaultBranchRefTargetCommit.model_rebuild()
GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistory.model_rebuild()
GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdges.model_rebuild()
GetRepoCommitsRepositoryDefaultBranchRefTargetCommitHistoryEdgesNode.model_rebuild()