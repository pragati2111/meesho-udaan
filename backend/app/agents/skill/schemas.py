"""
Skill Discovery Agent — output schema.

This is what the LLM must return, structured as a Pydantic model.
The prompt instructs the LLM to respond in JSON matching this shape exactly.
"""

from pydantic import BaseModel, Field


class SkillProfile(BaseModel):
    """
    Structured representation of a user's skill.
    Extracted from raw text, voice transcript, or image description.
    """

    skill_name: str = Field(
        description="Primary skill name, concise and marketable. E.g. 'Block Printing', 'Handloom Weaving'"
    )
    skill_category: str = Field(
        description="Broad category. E.g. 'Textile Arts', 'Food & Culinary', 'Handicrafts', 'Fashion'"
    )
    sub_skills: list[str] = Field(
        default_factory=list,
        description="Specific techniques or abilities within the main skill"
    )
    materials_required: list[str] = Field(
        default_factory=list,
        description="Raw materials or tools typically used"
    )
    experience_level: str = Field(
        description="Estimated experience level: beginner / intermediate / expert"
    )
    location_context: str = Field(
        default="",
        description="Any location mentioned or inferred. E.g. 'Rajasthan', 'South India'"
    )
    sellable_products: list[str] = Field(
        default_factory=list,
        description="Concrete products this skill can produce and sell online"
    )
    confidence_score: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Confidence in the extraction accuracy, 0.0 to 1.0"
    )