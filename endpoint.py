from fastapi import Depends, HTTPException, status, APIRouter

from models.database import session, User, Blog, Post, Subscribe
from schema import UserSchema, SubscribeSchema, UserResponseSchema, SubscribeResponseSchema, PostSchema

route = APIRouter()


@route.post('/user/add', status_code=201, response_model=UserResponseSchema, tags=['user'])
def user_add(data: UserSchema) -> str:
    user = User(username=data.username)
    blog = Blog(user=user)
    session.add(user)
    session.commit()

    return user


@route.post('/subscribe', status_code=201, response_model=SubscribeResponseSchema, tags=['subscribe'])
def user_subscribe(data: SubscribeSchema):
    # todo проверить подписку прежде чем добавить
    user = session.query(User).filter(User.id == data.user_id).one()
    subscribe = Subscribe(user_id=user.id, blog_id=data.blog_id)
    user.subscribers.append(subscribe)
    session.add(user)
    session.commit()

    return subscribe


@route.delete('/unsubscribe', status_code=200, response_model=SubscribeResponseSchema, tags=['subscribe'])
def user_subscribe(data: SubscribeSchema):
    subscribe = session.query(Subscribe).filter(Subscribe.user_id == data.user_id,
                                                Subscribe.blog_id == data.blog_id).one()

    session.delete(subscribe)
    session.commit()

    return subscribe


@route.get('/tape/{user_id}', status_code=200, response_model=list[PostSchema], tags=['tape'])
def tape(user_id: int):
    user = session.query(User).filter(User.id == user_id).one()
    posts = []
    for subscribe in user.subscribers:
        for post in subscribe.blog.post:
            posts.append(post.id)
    res = session.query(Post).filter(Post.id.in_(posts)).order_by(Post.created_at).all()

    return res


@route.get('/all/{user_id}', status_code=200)
def all_subscribe(user_id: int):
    user = session.query(User).filter(User.id == user_id).one()
    res = []
    for i in user.subscribers:
        res.append({'user_id': i.user_id,
                    'blog_id': i.blog_id})

    return res
