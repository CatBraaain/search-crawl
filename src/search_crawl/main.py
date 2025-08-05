from fastapi import FastAPI
from fastapi.routing import APIRoute

from .crawl.routing import router as crawl_router
from .healthz.healthz import router as healthz_router
from .search.routing import router as search_router
from .search_crawl.routing import router as search_crawl_router


def main() -> FastAPI:
    app = FastAPI()
    app.include_router(healthz_router)
    app.include_router(search_router)
    app.include_router(crawl_router)
    app.include_router(search_crawl_router)
    simplify_client_method_names(app)
    return app


def simplify_client_method_names(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


app = main()
