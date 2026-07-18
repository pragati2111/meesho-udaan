from pydantic import BaseModel, Field


class BrandIdentity(BaseModel):
    brand_name: str = Field(description="Memorable, pronounceable brand name")
    tagline: str = Field(description="Short emotional tagline under 8 words")
    color_palette: list[str] = Field(description="3-4 hex color codes")
    tone_of_voice: str = Field(description="How the brand communicates")
    target_persona: str = Field(description="One-sentence buyer persona")
    brand_story: str = Field(description="2-3 sentence origin story for the brand")