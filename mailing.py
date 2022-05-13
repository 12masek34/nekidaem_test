import requests
import schedule
import time


def mailer():
    ALL_USER = 'http://127.0.0.1:8000/user/all'
    TAPES_USER = 'http://127.0.0.1:8000/tape/limit_5/'

    subscribes = requests.get(ALL_USER).json()
    for subscribe in subscribes:
        username = subscribe['username']
        user_id = str(subscribe['id'])
        tapes = requests.get(TAPES_USER + user_id).json()
        if len(tapes["items"]) == 0:
            continue

        print(f'Рассылка постов для - {user_id}-{username}: \n {tapes["items"][0]}')


schedule.every().day.at("11:13").do(mailer)

while True:
    schedule.run_pending()
    time.sleep(1)
