from pydantic import BaseModel, Field


class MarketIntelligence(BaseModel):
    demand_level: str = Field(description="low / medium / high")
    market_size_estimate: str = Field(description="E.g. '2,400 Cr annually'")
    top_performing_categories: list[str] = Field(default_factory=list)
    competitor_count: int = Field(description="Approximate sellers on Meesho")
    avg_competitor_price: float = Field(description="Average price in INR")
    platform_opportunity: str = Field(description="Specific gap on Meesho")
    underserved_segments: list[str] = Field(default_factory=list)
    demand_rationale: str = Field(description="2-3 sentence explanation")