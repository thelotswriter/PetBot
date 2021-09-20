import time
import schedule


def update():
    print('Look ma, no hands!')


def run():
    print('Connected to engine!')
    schedule.every(5).seconds.do(update)
    while True:
        schedule.run_pending()
        time.sleep(1)
