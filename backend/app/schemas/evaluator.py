"""
Pydantic schemas for request and response validation
"""

from typing import List
from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    """Request model for privacy policy evaluation"""
    text: str = Field(..., min_length=10, description="Privacy policy text to evaluate")


class RiskPoint(BaseModel):
    """Individual risk point identified in the policy"""
    category: str = Field(..., description="Category of the risk (e.g., 'Data Collection', 'Third-Party Sharing')")
    description: str = Field(..., description="Description of the risk")
    severity: str = Field(..., description="Severity level: 'low', 'medium', or 'high'")


class EvaluateResponse(BaseModel):
    """Response model for privacy policy evaluation"""
    summary: str = Field(..., description="Simple language summary of the policy")
    risk_score: float = Field(..., ge=0, le=5, description="Overall risk score from 0 (very risky) to 5 (very safe)")
    risk_points: List[RiskPoint] = Field(..., description="List of identified risk points")

