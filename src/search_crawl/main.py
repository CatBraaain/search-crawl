from fastapi import FastAPI
from fastapi.routing import APIRoute

from .crawl.router import router as crawl_router
from .extract.router import router as extract_router
from .healthz.router import router as healthz_router
from .search.router import router as search_router


def main() -> FastAPI:
    app = FastAPI(
        license_info={
            "name": "WTFPL",
            "identifier": "WTFPL",
        },
    )
    app.include_router(healthz_router)
    app.include_router(search_router)
    app.include_router(crawl_router)
    app.include_router(extract_router)
    simplify_client_method_names(app)
    return app


def simplify_client_method_names(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


app = main()
