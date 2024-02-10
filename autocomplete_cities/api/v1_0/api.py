from typing import Optional
import re
from fastapi import APIRouter

import autocomplete_cities.suggestion.service as suggestion_service
import autocomplete_cities.api.v1_0.schemas as schemas

router = APIRouter(prefix="/api/v1.0")
only_letters_regex = re.compile("[^a-zA-Z]")


@router.get(
    "/suggestions",
    response_model=schemas.GetSuggestionsResponse,
    description="Get suggested cities"
)
async def get_suggestions(q: str, cutoff: Optional[float] = .50, latitude: Optional[float] = None, longitude: Optional[float] = None):
    q = only_letters_regex.sub("", q).lower()

    cities_by_score = suggestion_service.get_suggestions(q, latitude, longitude)
    all_cities = []
    for score, cities in cities_by_score.items():
        if score >= cutoff:
            for city in cities:
                all_cities.append(
                    schemas.Suggestion(
                        name=city.get_name(),
                        latitude=city.latitude,
                        longitude=city.longitude,
                        score=score
                    )
                )
        else:
            break

    return schemas.GetSuggestionsResponse(suggestions=all_cities)
