from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class RecipeBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2_000)
    ingredients: list[str] = Field(min_length=1)
    instructions: list[str] = Field(min_length=1)
    cooking_time_minutes: int = Field(gt=0, le=1_440)
    dietary_tags: list[str] = Field(default_factory=list)


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class RecipeSearchResult(BaseModel):
    recipe: RecipeResponse
    score: float