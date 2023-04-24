from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .metrics import add_metrics_middleware


def setup_middlewares(app: FastAPI):
    add_metrics_middleware(app)
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])
