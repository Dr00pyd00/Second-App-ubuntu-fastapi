from fastapi import FastAPI

from app.routers.post import router as post_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.posts_likes import router as post_like_router

from app.core.logging_config import setup_logging, get_logger

# Logger Setups ==================
setup_logging()
logger = get_logger(__name__)

logger.info("🚀 Fastapi App started!")


app = FastAPI()

# table autocreation:
#Base.metadata.create_all(bind=engine)

# ROUTERS:
app.include_router(post_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(post_like_router)

logger.info("✅ Routers charged!")


@app.get("/")
async def root():
    logger.info("root get visited")
    return {"message":"ROOT"}
