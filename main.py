from requests import get

from fetcher import fetch_data

# Initialize Stuff

# Forever Do:
last_traing = time.now()

while True:
    data = do_fetch()

    if time.now() - last_traing > 5min:
        do_train()
        last_traing = time.now()

    laps = do_count()

    do_push(laps)

    sleep(10)

