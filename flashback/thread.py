# -*- coding: utf-8 -*-

import re
import csv
import json
import datetime
from collections import Counter

import requests
from bs4 import BeautifulSoup


class Thread():

    def __init__(self, base_url):
        self.base_url = base_url
        self.posts = []

    def get_posts(self, pages=None):
        """Gets all comments in a given thread"""
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        page_count = pages or self.__get_page_count(soup)

        for page in range(1, page_count + 1):
            slug = 'p{page}'.format(page=str(page))
            url = ''.join([self.base_url, slug])
            page_posts = self.__get_page_posts(url)
            self.posts.extend(page_posts)

        return self

    def to_csv(self, fname):
        """Saves the posts to a CSV file"""
        with open(fname, 'w') as csvfile:
            headers = ['id', 'user_name', 'time', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for p in self.posts:
                row = {'id': p['id'].encode('utf-8'),
                       'user_name': p['user_name'].encode('utf-8'),
                       'time': p['time'].encode('utf-8'),
                       'content': p['content'].encode('utf-8')}
                writer.writerow(row)

    def to_json(self, fname):
        """Saves the posts to a JSON file"""
        pass

    def describe(self):
        counter = Counter([x['user_name'] for x in self.posts])
        common_authors = counter.most_common(5)
        return {
            'common_authors': common_authors
        }

    def __get_page_posts(self, url):
        """Gets all posts on a page"""
        parsed_posts = []
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        posts = soup.select('#posts > div')
        posts.pop()

        for post in posts:
            parsed_post = {}
            parsed_post['user_name'] = self.__get_post_user_name(post)
            parsed_post['user_id'] = self.__get_post_user_id(post)
            parsed_post['id'] = self.__get_post_id(post)
            parsed_post['time'] = self.__get_post_time(post)
            parsed_post['content'] = self.__get_post_content(post)
            parsed_posts.append(parsed_post)

        return parsed_posts

    def __get_post_time(self, post):
        """Extracts the timestamp from a post"""
        time_text = post.find('td', {'class': 'post-date'}).text.strip()
        if 'Idag' in time_text:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            return time_text[0:11].replace('Idag,', date)
        else:
            return time_text[0:17].replace(',', '')

    def __get_post_user_name(self, post):
        """Extracts the user name from a post"""
        return post.select_one('a.bigusername').text

    def __get_post_user_id(self, post):
        """Extracts the user id from a post"""
        return post.select_one('a.bigusername')['href']

    def __get_post_id(self, post):
        """Extracts the id of a post"""
        return post.select_one('span.fr a')['href']

    def __get_post_content(self, post):
        """Extracts the id of a post"""
        content = post.select_one('div.post_message')
        quotes = content.find_all('div', {'class': 'post-quote-holder'})
        for quote in quotes:
            quote_text = re.sub('\n+', '\n', quote.text.strip())
            quote_text = quote_text.replace(u'\xa0', '')
            quote_text = quote_text.replace(u'\xc2', '')
            quote_text = quote_text.replace(u'\t', '')
            quote.replace_with(u'[FQ]{}[EFQ]'.format(quote_text))

        spoilers = content.find_all('div', {'class': 'post-bbcode-spoiler'})
        for spoiler in spoilers:
            spoiler.replace_with(u'[FSP]{}[EFP]'.format(spoiler.text.strip()))

        return content.text.strip()

    def __get_page_count(self, soup):
        """Finds the number of pages for the given thread
        <td class="vbmenu_control smallfont2 delim">Sidan 1 av 15</td>
        """
        element = soup.select_one('td.vbmenu_control.smallfont2.delim')
        if element:
            page_count = element.text.split(' ')[-1]
            return int(page_count)
        return 1

    def __getitem__(self, index):
        return self.posts[index]

    def __len__(self):
        return len(self.posts)

    def __repr__(self):
        return '<Flashback.Thread {}>'.format(self.base_url)

    def __iter__(self):
        return iter(self.posts)
