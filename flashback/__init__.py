from . import Flashback


def get(base_url):
    thread = Flashback.Thread(base_url)
    thread.get_posts()
    return thread
