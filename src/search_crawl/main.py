from fastapi import FastAPI
from fastapi.routing import APIRoute

from .routers import crawl, healthz, search, search_crawl


def main() -> FastAPI:
    app = FastAPI()
    app.include_router(healthz.router)
    app.include_router(search.router)
    app.include_router(crawl.router)
    app.include_router(search_crawl.router)
    simplify_client_method_names(app)
    return app


def simplify_client_method_names(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


app = main()
