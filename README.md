Flashback is a Python scraper for the Swedish bulletin board site flashback.org. The scraper does one thing, and it does it well.

```python
>>> import flashback
>>> thread = flashback.get('https://www.flashback.org/t2629982')
>>> thread.title
u'Min hund morrar åt mig'
>>> len(thread)
47
```

##Installation
Use pip to install Flashback.

```
$ pip install flashback
```

##Usage
Scrape a thread/discussion.
```python
url = 'https://www.flashback.org/<some-url>'
thread = flashback.get(url)
```

Iterate over the posts. Each post is a dict with the following keys: id, user_name, time and content. They should be quite self-explanatory.
```python
for post in thread:
    print post['content']
```

Get a single post by index.
```python
thread[23]
```

Get a summary of the thread's basic facts, like most common authors.
```python
thread.describe()
```

Save the whole thread to a CSV or JSON file.
```python
thread.to_csv('some_discussion.csv')
thread.to_json('some_discussion.json')
```
