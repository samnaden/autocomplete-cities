from autocomplete_cities.data.service import get_cities


def test_get_cities():
    cities = get_cities()
    assert len(cities) == 5339
