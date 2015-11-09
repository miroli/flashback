from thread import Thread
from post import Post


def get(base_url):
    t = Thread(base_url)
    t.get()
    return t
