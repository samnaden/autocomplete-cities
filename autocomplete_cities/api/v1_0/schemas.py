from pydantic import BaseModel


class Suggestion(BaseModel):
    name: str
    latitude: str
    longitude: str
    score: float


class GetSuggestionsResponse(BaseModel):
    suggestions: list[Suggestion]
