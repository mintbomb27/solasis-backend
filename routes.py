from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Sensor, SensorValue

router = APIRouter()

@router.post("/", response_description="Create sensor", status_code=status.HTTP_201_CREATED, response_model=Sensor)
def create_sensor(request: Request, sensor: Sensor = Body(...)):
    sensor = jsonable_encoder(sensor)
    new_sensor = request.app.database["solasis"]["sensors"].insert_one(sensor)
    created_sensor = request.app.database["solasis"]["sensors"].find_one(
        {"_id": new_sensor.inserted_id}
    )
    print(created_sensor)
    return created_sensor

@router.post("/value", response_description="Update the sensor value", status_code=status.HTTP_201_CREATED, response_model=SensorValue)
def insert_sensor_value(request: Request, sensor_val: SensorValue = Body(...)):
    sensor_val = jsonable_encoder(sensor_val)
    new_val = request.app.database["solasis"]["sensor_values"].insert_one(sensor_val)
    inserted_val = request.app.database["solasis"]["sensor_values"].find_one(
        {"_id": new_val.inserted_id}
    )
    return inserted_val

@router.get("/all", response_description="Get all sensors", response_model=List[Sensor])
def get_sensors(id: str, request: Request):
    sensors = list(request.app.database["solasis"]["sensors"].find(limit=100))
    return sensors

@router.get("/{id}", response_description="Get a sensor", response_model=Sensor)
def get_sensor(id: str, request: Request):
    if (sensor := request.app.database["solasis"]["sensors"].find_one({"_id": id})) is not None:
        return sensor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor with ID {id} not found")

@router.get("/value/{id}", response_description="Get the latest sensor value", response_model=SensorValue)
def get_latest_val(id: str, request: Request):
    try:
        if (sensor_val := request.app.database["solasis"]["sensor_values"].find({"sensor_id": id}).sort("timestamp",-1).limit(1)) is not None:
            return sensor_val[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor with ID {id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor with ID {id} not found")