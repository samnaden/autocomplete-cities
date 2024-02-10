FROM python:3.12

RUN mkdir /autocomplete-cities
WORKDIR /autocomplete-cities

COPY ./pyproject.toml /autocomplete-cities/pyproject.toml
COPY ./poetry.lock /autocomplete-cities/poetry.lock
COPY ./autocomplete_cities /autocomplete-cities/autocomplete_cities

RUN pip3 install poetry==1.3.2 && poetry install

CMD ["poetry", "run", "uvicorn", "autocomplete_cities.app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]
