# -*- coding: utf-8 -*-

import csv
import json
import datetime
import urllib
from collections import Counter

import requests
from bs4 import BeautifulSoup

from .post import Post


class TrashException(Exception):
    pass


class AuthException(Exception):
    pass


class LoginException(Exception):
    pass


class NotFoundException(Exception):
    pass


errors = [
    ((u'Denna tråd har flyttats till "Papperskorgen". '
      u'Ett delforum för trådar med för låg kvalitet.'),
     TrashException('Login required for threads in trashcan.')),
    ((u'du har inte behörighet till den här sidan. '
     u'Det kan bero på en av flera anledningar:'),
     AuthException('Your account lacks sufficient permissions.')),
    ((u'Du är inte inloggad eller också har du inte behörighet'
      u' att se den här sidan. Det kan bero på en av flera'),
     LoginException('Login required for this particular thread.')),
    ((u'Du angav ett ogiltigt Ämne. Om du följde en giltig'
      u' länk, var vänlig och kontakta den'),
     NotFoundException('Thread does not exist.')),
    ((u'Inget Ämne specifierat. Om du följde en giltig'
      u' länk var vänlig och meddela den'),
     NotFoundException('Thread does not exist.')),
]


class Thread():
    """Temp"""
    def __init__(self, base_url):
        self.base_url = base_url
        self.posts = []

    def get(self, requests=requests):
        r = requests.get(self.base_url)
        self.start = BeautifulSoup(r.text, 'html.parser')

        for message, thread_exception in errors:
            if message in self.start.text:
                raise thread_exception

        self.append_page(self.start)
        page_count = self._get_page_count(self.start)

        for page in range(2, page_count + 1):
            slug = 'p{page}'.format(page=str(page))
            url = ''.join([self.base_url, slug])
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            self.append_page(soup)

    def append_page(self, soup):
        for div in soup.select('#posts > div')[:-1]:
            self.append_post(div)

    def append_post(self, soup):
        post = Post(soup)
        self.posts.append(post)

    def describe(self):
        counter = Counter([x['user_name'] for x in self.posts])
        common_authors = counter.most_common(5)
        return {
            'common_authors': common_authors
        }

    @property
    def title(self):
        """Title of thread"""
        return self.start.title.text[0:-18]

    @property
    def section(self):
        navbar = self.start.find('table', {'class': 'forum-navbar'})
        breadcrumbs = navbar.find('tr', {'valign': 'bottom'}).find_all('a')
        section = breadcrumbs[-1]
        return {'id': section['href'][1:], 'name': section.text}

    def _get_page_count(self, soup):
        """Finds the number of pages for the given thread
        <td class="vbmenu_control smallfont2 delim">Sidan 1 av 15</td>
        """
        element = soup.select_one('td.vbmenu_control.smallfont2.delim')
        if element:
            page_count = element.text.split(' ')[-1]
            return int(page_count)
        return 1

    def to_csv(self, fname):
        """Saves the posts to a CSV file"""
        with open(fname, 'w') as csvfile:
            headers = ['id', 'user_name', 'time', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for p in self.posts:
                row = {'id': p.id.encode('utf-8'),
                       'user_name': p.user_name.encode('utf-8'),
                       'time': p.timestamp.encode('utf-8'),
                       'content': p.content.encode('utf-8')}
                writer.writerow(row)

    def to_json(self, fname):
        """Saves the posts to a JSON file"""
        out = {
            'title': self.title,
            'posts': self.posts
        }

        with open(fname, 'w') as f:
            f.write(json.dumps(out))

    def __getitem__(self, index):
        return self.posts[index]

    def __len__(self):
        return len(self.posts)

    def __repr__(self):
        return '<Flashback.Thread {}>'.format(self.base_url)

    def __iter__(self):
        return iter(self.posts)
