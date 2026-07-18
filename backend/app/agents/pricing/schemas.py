from pydantic import BaseModel, Field


class PricingStrategy(BaseModel):
    base_price: float = Field(description="Minimum viable price in INR")
    recommended_price: float = Field(description="Optimal price for margin and volume")
    premium_price: float = Field(description="Price for gift or premium segment")
    currency: str = Field(default="INR")
    margin_percentage: float = Field(description="Profit margin at recommended price")
    pricing_rationale: str = Field(description="Why this price was chosen")
    discount_strategy: str = Field(description="When and how to offer discounts")