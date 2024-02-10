import functools
import math
import geopy.distance


@functools.lru_cache(maxsize=int(math.pow(2, 16)))
def get_distance_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    return geopy.distance.geodesic(a, b).km
