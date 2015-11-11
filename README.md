![Flashback version](https://img.shields.io/pypi/v/flashback.svg)
![Flashback downloads](https://img.shields.io/pypi/dm/flashback.svg)

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

##### Scrape a thread/discussion.
```python
url = 'https://www.flashback.org/<some-url>'
thread = flashback.get(url)
```

Each thread has the following attributes:

* thread_name
* thread_id
* section_id
* section_name

Each post in the thread is an object with the following attributes:

* id
* user_name
* user_id
* timestamp
* content

##### Iterate over the posts.

```python
for post in thread:
    print post.content
```

##### Get a single post by index.
```python
thread[23]
```

##### Get thread summary
Returns a summary of the thread's basic facts, like most common authors.
```python
thread.describe()
```

##### Save to file
Supported output formats are CSV and JSON.
```python
thread.to_csv('some_discussion.csv')
thread.to_json('some_discussion.json')
```

##Formatting

Some posts contain specially formatted HTML elements, such as quote containers and hidden spoilers. These HTML tags are parsed and formatted using a simple notation.

##### Quotes
Quotes begin with `[FQ]` and end with `[EFQ]`.
```
[FQ]This is a quote in a post[EFQ]
This is the actual content of the post.
```

##### Spoilers
Spoilers begin with `[FSP]` and end with `[EFP]`.
```
[FSP]This is a hidden spoiler[EFP]
This is normal text content.
```

##### Links
Flashback prepends all external links with `https://www.flashback.org/leave.php?u=<some-url>` which is a transit page users have to click through to get out of Flashback. In parsing these links, the transit page part of the href is removed.

The parsed link contains the original href value and the original text content. In cases where the link has just been pasted into the post, these two values are identical. The parsed link is wrapped in `[FA]` and `[EFA]`.

Original link:

    <a href="http://example.com">Look at this</a>

Link in Flashback post:

    <a href="https://www.flashback.org/leave.php?u=http://example.com">Look at this</a>

Parsed link result:

    [FA]http://example.com Look at this[EFA]

##### Timestamps
Timestamps are converted to naive Python datetime objects, and represent the `Europe/Stockholm` timezone.