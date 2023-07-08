from fastapi import APIRouter

from . import ping, post

main_api_router = APIRouter()

main_api_router.include_router(ping.router)
main_api_router.include_router(post.router)
