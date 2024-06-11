# depends.py

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from controller import userController, type_nnController, chatsController, status_messageController, authController, alertsController
import messagesController
from pydantic import BaseModel
from config import AppConfig
from fastapi.middleware.cors import CORSMiddleware

# Dependency Injection
def configure_app(app: FastAPI, config: AppConfig):
    # Adding CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.get("/")
    def index():
        return {"msg": "Перейдите на /docs для документации по API"}

    # Include routers
    app.include_router(userController.router)
    app.include_router(type_nnController.router)
    app.include_router(chatsController.router)
    app.include_router(alertsController.router)
    app.include_router(status_messageController.router)
    app.include_router(messagesController.router)
    app.include_router(authController.router)

    # Define Pydantic model for LLM query
    class LLMQuery(BaseModel):
        context: str
        question: str

    # Register Tortoise ORM
    register_tortoise(
        app,
        db_url=config.db_url,
        modules={"models" : ["models.userModels", "models.chatModels", "models.messageModels", "models.status_messageModels", "models.type_nnModels", "models.alertsModels"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
