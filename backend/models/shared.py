from pydantic import BaseModel, Field
from uuid import UUID

class BaseModelWithId(BaseModel):
    id: UUID = Field(..., alias="id")

    class Config:
        allow_population_by_field_name = True
