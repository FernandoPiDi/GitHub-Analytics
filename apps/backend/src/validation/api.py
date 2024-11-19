"""
Set of types to validate the API requests and responses.
"""

from pydantic import BaseModel


class AnalyticsRequest(BaseModel):
    """
    Request body for the analytics endpoint.
    The analytics endpoint is used to generate charts
    in typescript from the repository using Natural Language.

    Attributes:
        message: The user prompt.
        owner: The owner of the repository.
        repo: The repository to analyze.
    """

    message: str
    owner: str
    repo: str
