import uuid
from typing import Optional
from pydantic import BaseModel, FiniteFloat, Field
import datetime

class Sensor(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True

class SensorValue(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    sensor_id: str = Field(default_factory=uuid.uuid4)
    value: float = FiniteFloat()
    timestamp: datetime.datetime = datetime.datetime.now()
