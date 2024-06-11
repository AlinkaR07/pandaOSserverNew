# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from depends import configure_app
from config import AppConfig

app = FastAPI()

configure_app(app, AppConfig)
