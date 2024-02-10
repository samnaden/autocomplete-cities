from typing import Optional

import autocomplete_cities.data.service as data_service
import autocomplete_cities.data.schemas as data_schemas
import autocomplete_cities.util.string_similarity as string_similarity
import autocomplete_cities.util.location_similarity as location_similarity

cities = data_service.get_cities()


def get_suggestions(city_name: str, lat: Optional[float], long: Optional[float]) -> dict[float, list[data_schemas.City]]:
    """a ranking mechanism that gives equal weight to name similarity and location similarity (if location provided)"""

    max_distance = -1.0
    similarities = {}
    # TODO: parallelize this for loop
    for city_id, city in cities.items():
        name_similarity = string_similarity.get_similarity_score(city_name, city.name)
        similarities[city_id] = [name_similarity]

        if lat is not None and long is not None:
            distance = location_similarity.get_distance_km((lat, long), (city.latitude, city.longitude))
            similarities[city_id].append(distance)
            max_distance = max(max_distance, distance)

    if max_distance > -1.0:
        # scale the distances to range [0, 1] - give lower scores to further away cities
        for city_id, scores in similarities.items():
            scores[1] = 1 - (scores[1] / max_distance)

    cities_by_score = {}
    for city_id, scores in similarities.items():
        if len(scores) == 2:
            score = round(scores[0] * .5 + scores[1] * .5, 2)
        else:
            score = round(scores[0], 2)

        if score in cities_by_score:
            cities_by_score[score].append(cities[city_id])
        else:
            cities_by_score[score] = [cities[city_id]]

    cities_by_score_sorted = dict(sorted(cities_by_score.items(), key=lambda x: x[0], reverse=True))

    return cities_by_score_sorted
