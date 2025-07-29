from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "OK"
