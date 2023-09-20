import base64
import json
import time
import pickle
# from post import Post
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["10.11.101.129:9092"])

def push_kafka(posts, comments):
    if len(posts) > 0:
        bytes_obj = pickle.dumps([ob.__dict__ for ob in posts])
        producer.send('lnmxh', bytes_obj)
        if len(comments) > 0:
            bytes_obj = pickle.dumps([ob.__dict__ for ob in comments])
            producer.send('lnmxh', bytes_obj)
        return 1  
    else:
        return 0
    
  

class GeneratorPost:
    def __init__(self, target, args: list = []) -> None:
        self.target = target
        self.args = args
    def run(self):
        for posts in self.target(*self.args):
            print(f"số bài post group đẩy qua kafka là {len(posts)}")
            push_kafka(posts=posts, comments=None)
            # for post in posts:
            #     write_log_post(post)
                # if self.is_return:
                #     return post
    def get_posts(self, list_posts: list):
        for posts in self.target(*self.args):
            print(f"số bài posts là {len(posts)}")
            list_posts.extend(posts)
            push_kafka(posts=posts, comments=None)
            # for post in posts:
            #     write_log_post(post)
                