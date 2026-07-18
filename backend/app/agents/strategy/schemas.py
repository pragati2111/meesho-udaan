from pydantic import BaseModel, Field


class BusinessStrategy(BaseModel):
    recommended_product: str = Field(description="Single best product to launch first")
    product_description: str = Field(description="2-3 sentence product description")
    business_model: str = Field(description="E.g. 'D2C via Meesho'")
    target_segment: str = Field(description="Specific customer segment")
    target_cities: list[str] = Field(default_factory=list)
    differentiation_strategy: str = Field(description="What makes this seller unique")
    key_risks: list[str] = Field(default_factory=list)
    rationale: str = Field(description="Why this strategy was chosen")