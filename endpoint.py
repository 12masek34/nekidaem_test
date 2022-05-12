from fastapi import Depends, HTTPException, status, APIRouter
from fastapi_pagination import paginate
from fastapi import FastAPI
from fastapi_pagination.bases import AbstractPage
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session

from pagination import Page
from models.database import User, Blog, Post, Subscribe, get_db
from models.cache import redis
from schema import UserSchema, SubscribeSchema, UserResponseSchema, SubscribeResponseSchema, PostSchema

app = FastAPI()


@app.post('/user/add', status_code=201, response_model=UserResponseSchema, tags=['user'])
async def user_add(data: UserSchema, db: Session = Depends(get_db)) -> UserSchema:
    user = User(username=data.username)
    blog = Blog(user=user)
    db.add(user)
    db.commit()

    return user


@app.post('/subscribe', status_code=201, response_model=SubscribeResponseSchema, tags=['subscribe'])
async def user_subscribe(data: SubscribeSchema, db: Session = Depends(get_db)) -> SubscribeResponseSchema:

    try:
        user = db.query(User).filter(User.id == data.user_id).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    subscribe = Subscribe(user_id=user.id, blog_id=data.blog_id)
    user.subscribers.append(subscribe)
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Blog not found'
        )

    return subscribe


@app.delete('/unsubscribe', status_code=200, response_model=SubscribeResponseSchema, tags=['subscribe'])
async def user_subscribe(data: SubscribeSchema, db: Session = Depends(get_db)) -> SubscribeResponseSchema:
    subscribe = db.query(Subscribe).filter(Subscribe.user_id == data.user_id,
                                           Subscribe.blog_id == data.blog_id).one()

    db.delete(subscribe)
    db.commit()

    return subscribe


@app.get('/tape/{user_id}', status_code=200, response_model=Page[PostSchema], tags=['tape'])
async def tape(user_id: int, post_id: int | None = None, db: Session = Depends(get_db)) -> AbstractPage[PostSchema]:
    if post_id is not None:
        await redis.lpush(user_id, post_id)
    try:
        user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    posts = []
    cache = await redis.lrange(user_id, 0, -1)

    for subscribe in user.subscribers:
        for post in subscribe.blog.post:
            if str(post.id) in cache:
                continue
            posts.append(post.id)

    return paginate(db.query(Post).filter(Post.id.in_(posts)).order_by(Post.created_at).all())


@app.get('/all/{user_id}', status_code=200)
async def all_subscribe(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).one()
    res = []
    for i in user.subscribers:
        res.append({'user_id': i.user_id,
                    'blog_id': i.blog_id})

    return res
