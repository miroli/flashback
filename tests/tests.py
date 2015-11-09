# -*- coding: utf-8 -*-

import os
import unittest
import flashback

from bs4 import BeautifulSoup


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class FakeRequests():
    def get(self, url):
        with open(os.path.join(__location__, 'sample_page.html'), 'r') as f:
            return FakeResponse(f.read())


class FakeResponse():
    status_code = 200

    def __init__(self, text):
        self.text = text


class ThreadTestCase(unittest.TestCase):
    def setUp(self):
        fake_requests = FakeRequests()
        self.t = flashback.Thread('http://test.com')
        self.t.get(requests=fake_requests)

    def test_page_count_when_over_one(self):
        html = '<td class="vbmenu_control smallfont2 delim">Sidan 1 av 15</td>'
        soup = BeautifulSoup(html, 'html.parser')
        t = flashback.Thread('http://test.com')
        count = t._get_page_count(soup)
        self.assertEqual(count, 15)

    def test_page_count_when_one(self):
        count = self.t._get_page_count(self.t.start)
        self.assertEqual(count, 1)

    def test_title(self):
        self.assertEqual(self.t.title, u'Dansk minister avvisar multikulti')

    def test_posts_are_appended(self):
        self.assertEqual(len(self.t.posts), 5)

    def test_section_name_is_found(self):
        self.assertEqual(self.t.section['name'],
                         u'Nationalsocialism, fascism och nationalism')

    def test_section_id_is_found(self):
        self.assertEqual(self.t.section['id'], u'f34')


class PostTestCase(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(__location__, 'sample_post.html'), 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            self.p = flashback.Post(soup)

    def test_post_id(self):
        self.assertEqual(self.p.id, u'/sp314812')

    def test_timestamp(self):
        self.assertEqual(self.p.timestamp, '2000-09-06 18:09')

    def test_user_name(self):
        self.assertEqual(self.p.user_name, u'Ördög (old)')

    def test_user_id(self):
        self.assertEqual(self.p.user_id, u'/u32584')

    def test_content(self):
        self.assertIn(u'mycket läsvärd artikel', self.p.content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
