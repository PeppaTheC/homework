"""This module contains realization of  pikabu pasres.

Pikabu parser gets specified number of posts and counts all tags.

Info: to get cookie you need to go and log in at https://pikabu.ru,
then open a Request Headers (Request URL: https://pikabu.ru/) and copy cookie to file user_cookie as
cookie = ...(ur cookie)

    Typical usage example:

        number_of_posts = 100
        session = requests.Session()
        posts_tags = pikabu_parser(session, number_of_posts)
"""

from bs4 import BeautifulSoup as bs
from collections import Counter
import requests
import user_cookie


HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Connection': 'keep-alive',
           'Cookie': user_cookie.cookie,
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78 (Edition Yx)',
           'Upgrade-Insecure-Requests': '1'}


def pikabu_parser(session: requests.Session, num_posts: int) -> Counter:
    """Parser tags in pikabu subscriptions on specified number of posts

    Args:
        session: Current session
        num_posts: Number of posts where we count tags

    Returns:
        Counter structure where key is name of tags and value it's number of appearances
        on specified number of posts
    """
    count = Counter()
    current_post = 0
    url = 'https://pikabu.ru/subs'
    max_pages_number = num_posts // 10 if not num_posts % 10 else num_posts // 10 + 1
    for page in range(max_pages_number + 1):
        paramload = {'page': str(page)}
        resp = session.get(url, headers=HEADERS, params=paramload)
        soup = bs(resp.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'story__tags tags'})
        for div in divs:
            current_post += 1
            for a in div:
                try:
                    count[a['data-tag']] += 1
                except (TypeError, KeyError):
                    pass
        if current_post == num_posts:
            return count


if __name__ == '__main__':
    number_of_posts = 100
    session = requests.Session()
    posts_tags = pikabu_parser(session, number_of_posts)
    with open('output/tag_statistics.dat', 'w') as stat_file:
        for key, value in posts_tags.most_common(10):
            stat_file.write(f"{key}: {value}\n")
