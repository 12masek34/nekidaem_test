import requests
import schedule
import time

ALL_USER = 'http://127.0.0.1:8000/user/all'
TAPES_USER = 'http://127.0.0.1:8000/tape/limit_5/'


def mailer():
    """Берет всех юзеров по апи, потом для каждого юзера, берет 5 последних постов из его ленты.
    Если тут будет много юзеров, лучше добавить пагинацию."""

    users = requests.get(ALL_USER).json()
    for user in users:
        username = user['username']
        user_id = str(user['id'])
        tapes = requests.get(TAPES_USER + user_id).json()
        if len(tapes["items"]) == 0:
            continue

        print(f'Рассылка постов для - {user_id}-{username}: \n {tapes["items"][0]}')


schedule.every().day.at("10:00").do(mailer)

while True:
    schedule.run_pending()
    time.sleep(1)
