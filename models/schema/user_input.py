from typing import Annotated, Literal

from pydantic import BaseModel, Field, computed_field, field_validator

try:
    from config.city_tier import tier_1_cities, tier_2_cities
except ImportError:
    from models.config.city_tier import tier_1_cities, tier_2_cities


class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0, lt=120)]
    height: Annotated[float, Field(..., gt=0, lt=2.5)]
    income_lpa: Annotated[float, Field(..., gt=0, lt=120)]
    city: Annotated[str, Field(...)]
    smoker: Annotated[bool, Field(...)]
    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        Field(...),
    ]

    @field_validator("city")
    @classmethod
    def normalize_city(cls, value: str) -> str:
        return value.strip().title()

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        if self.smoker and self.bmi > 27:
            return "medium"
        return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        if self.age < 45:
            return "adult"
        if self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        if self.city in tier_2_cities:
            return 2
        return 3
