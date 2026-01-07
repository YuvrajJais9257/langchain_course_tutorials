from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional

class Source(BaseModel):
    """Schema for a source used by the agent"""
    url: str = Field(..., description="The URL of the source")
    title: str = Field(..., description="The title of the job or page")

class AgentResponse(BaseModel):
    """Schema for the response from the agent with answer and sources."""
    answer: str = Field(..., description="The summary answer from the agent.")
    source: List[Source] = Field(default_factory=list, description="List of sources/jobs found.")