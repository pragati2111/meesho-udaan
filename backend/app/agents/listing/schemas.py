from pydantic import BaseModel, Field


class ListingContent(BaseModel):
    title: str = Field(description="SEO-optimised product title under 100 characters")
    description: str = Field(description="Compelling product description with bullet points")
    keywords: list[str] = Field(description="8-10 search keywords buyers use on Meesho")
    hindi_title: str = Field(description="Product title translated to Hindi")
    hindi_description: str = Field(description="Short 2-line Hindi description")
    category_path: str = Field(description="Meesho category path. E.g. 'Women > Ethnic Wear > Kurtas'")