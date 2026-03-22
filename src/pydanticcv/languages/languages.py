from pydantic import Field, BaseModel
from pydantic_extra_types.language_code import ISO639_3


class Language(BaseModel):
    name: str = Field(..., default_factory=str)
    iso: ISO639_3 = Field(..., default_factory=ISO639_3)
    native: bool = Field(..., default_factory=bool)
    # TODO level: Optional[]
