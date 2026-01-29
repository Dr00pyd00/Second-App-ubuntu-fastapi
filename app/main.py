from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.post import Post
from app.models.users import User
from app.models.posts_likes import PostLike
from app.routers.post import router as post_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.posts_likes import router as post_like_router


app = FastAPI()

# table autocreation:
#Base.metadata.create_all(bind=engine)

# ROUTERS:
app.include_router(post_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(post_like_router)


@app.get("/")
async def root():
    return {"message":"ROOT"}

