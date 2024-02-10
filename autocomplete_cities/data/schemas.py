from pydantic import BaseModel


class City(BaseModel):
    id: str
    name: str
    name_raw: str
    latitude: float
    longitude: float
    country: str
    region: str

    def get_name(self) -> str:
        return f"{self.name_raw}, {self.country}, {self.region}"
