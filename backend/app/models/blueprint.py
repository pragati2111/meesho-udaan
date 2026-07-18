from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
import uuid


class ProductRecommendation(BaseModel):
    name: str
    category: str
    description: str
    target_audience: str
    unique_selling_point: str


class MarketInsight(BaseModel):
    demand_level: Literal["low", "medium", "high"]
    trend: Literal["declining", "stable", "growing", "viral"]
    competitors: int
    opportunity: str
    seasonality: str | None = None


class PricingStrategy(BaseModel):
    base_price: float
    recommended_price: float
    premium_price: float
    currency: str = "INR"
    margin_percentage: float
    rationale: str


class BrandIdentity(BaseModel):
    brand_name: str
    tagline: str
    color_palette: list[str]
    tone_of_voice: str
    target_persona: str


class ListingContent(BaseModel):
    title: str
    description: str
    keywords: list[str]
    hindi_title: str | None = None
    hindi_description: str | None = None


class GrowthPlan(BaseModel):
    week1: list[str]
    month1: list[str]
    month3: list[str]
    channels: list[str]


class AgentResult(BaseModel):
    agent_id: str
    agent_name: str
    status: Literal["completed", "error"]
    duration_ms: int


class BusinessBlueprint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    skill_input: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product: ProductRecommendation
    market: MarketInsight
    pricing: PricingStrategy
    brand: BrandIdentity
    listing: ListingContent
    growth: GrowthPlan
    agents: list[AgentResult] = []


class GenerateRequest(BaseModel):
    skill_text: str | None = None
    skill_image_url: str | None = None
    skill_audio_url: str | None = None
    language: Literal["en", "hi"] = "en"


class GenerateResponse(BaseModel):
    blueprint_id: str
    status: Literal["processing", "completed", "error"]
    message: str = ""