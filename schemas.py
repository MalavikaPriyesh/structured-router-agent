from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class RouteDecision(BaseModel):
    category: Literal["billing", "technical_bug", "general_inquiry"] = Field()
    urgency: Literal["low", "medium", "high", "critical"] = Field()
    reasoning: str = Field(description="1 sentence explanation of this decision")

class TechnicalBugReport(BaseModel):
    issue_summary: str = Field()
    device_or_os: Optional[str] = Field(default="Unknown")
    error_codes: List[str] = Field(default_factory=list)
    reproduction_steps: List[str] = Field(default_factory=list)
    customer_sentiment: Literal["frustrated", "neutral", "confused", "angry"] = Field()

class BillingInquiry(BaseModel):
    account_id: Optional[str] = Field(default="Not provided")
    disputed_amount: Optional[float] = Field(default=None)
    currency: str = Field(default="USD")
    issue_type: Literal["refund_request", "overcharge", "cancellation", "payment_failed", "other"] = Field()
    action_required: str = Field()