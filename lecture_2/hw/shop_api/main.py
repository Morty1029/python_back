from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.routes import router

# Запуск job для 2 hw

app = FastAPI(title="hw3")

app.include_router(router)
Instrumentator().instrument(app).expose(app)
