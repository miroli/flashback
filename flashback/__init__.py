from . import thread


def get(base_url, pages=None):
    t = thread.Thread(base_url)
    t.get_posts(pages)
    return t
