from pydantic import BaseModel, Field


class GrowthPlan(BaseModel):
    week1_actions: list[str] = Field(description="Immediate actions in the first 7 days")
    month1_actions: list[str] = Field(description="Actions to take in the first month")
    month3_actions: list[str] = Field(description="Scale actions by month 3")
    recommended_channels: list[str] = Field(description="Sales and marketing channels to use")
    first_revenue_estimate: str = Field(description="Realistic first month revenue estimate")
    scale_trigger: str = Field(description="The signal that means it is time to scale up")