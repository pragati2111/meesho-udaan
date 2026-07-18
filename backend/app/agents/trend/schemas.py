from pydantic import BaseModel, Field


class TrendAnalysis(BaseModel):
    trend_direction: str = Field(description="declining / stable / growing / viral")
    growth_rate_estimate: str = Field(description="E.g. '42% YoY'")
    seasonal_peaks: list[str] = Field(default_factory=list)
    emerging_niches: list[str] = Field(default_factory=list)
    consumer_sentiment: str = Field(description="How buyers feel about this category")
    recommended_launch_window: str = Field(description="Best time to launch")
    trend_rationale: str = Field(description="2-3 sentence explanation")