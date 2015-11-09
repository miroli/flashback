# -*- coding: utf-8 -*-

import re
import datetime
import urllib


class Post():
    def __init__(self, soup):
        self.soup = soup

    @property
    def timestamp(self):
        """Extracts the timestamp from a post"""
        time_text = self.soup.find('td', {'class': 'post-date'}).text.strip()
        if 'Idag' in time_text:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            return time_text[0:11].replace('Idag,', date)
        if u'Igår' in time_text:
            now = datetime.datetime.now()
            date = (now - datetime.timedelta(hours=24)).strftime('%Y-%m-%d')
            return time_text[0:11].replace(u'Igår,', date)
        else:
            return time_text[0:17].replace(',', '')

    @property
    def user_name(self):
        """Extracts the user name from a post"""
        try:
            user_name = self.soup.select_one('a.bigusername').text
        except AttributeError:
            user_name = ''
        return user_name

    @property
    def user_id(self):
        """Extracts the user id from a post"""
        try:
            user_id = self.soup.select_one('a.bigusername')['href']
        except TypeError:
            user_id = ''
        return user_id

    @property
    def id(self):
        """Extracts the id of a post"""
        return self.soup.select_one('span.fr a')['href']

    @property
    def content(self):
        """Extracts the id of a post"""
        content = self.soup.select_one('div.post_message')
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

        links = content.find_all('a')
        for link in links:
            try:
                href = urllib.unquote(link['href'].split('.php?u=')[1])
                link.replace_with(u'[FA]{} {}[EFA]'.format(href,
                                                           link.text).strip())
            except IndexError:
                continue

        return content.text.strip()
