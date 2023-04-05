from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from pymongo import MongoClient
from routes import router as sensor_router
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.getenv("ATLAS_URI"))
    app.database = app.mongodb_client[os.getenv("DB_NAME")]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(sensor_router, tags=["sensors"], prefix="/sensor")