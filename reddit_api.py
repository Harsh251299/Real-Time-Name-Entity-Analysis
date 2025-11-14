import praw
from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime

reddit = praw.Reddit(
    client_id="hi75yb0tGP5lGeemjlIaGw",
    client_secret="NqtEZ_gmWT6_ta0CJ_2aAgxIlQgFuA",
    password="WcPC#5gYfs8mq4.",
    user_agent="ChangeMeClient/0.1 by Dhairya22",
    username="Dhairya22",
)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for submission in reddit.subreddit("all").stream.submissions():
    timestamp = datetime.now().timestamp()
    message = {'timestamp': timestamp, 'submission': submission.selftext}
    # data = {'submission':submission.selftext}
    producer.send('reddit', value=message)
    sleep(5)