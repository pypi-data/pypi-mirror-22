import re
from bs4 import BeautifulSoup
import bs4
from fundoshi.classes import objdict
from ..utils import cfscraper
from .decoder import decode_url, get_key

_get = cfscraper.get
_post = cfscraper.post


class Kissmanga(object):

    netlocs = ['kissmanga.com']
    name = 'kissmanga'

    # Return a list of objdicts that store name, url, and site:
    # [{'name': 'Naruto', 'url': 'http://...', 'site': kissmanga}, ...]
    def search_series(self, keyword):
        url = 'http://kissmanga.com/Search/SearchSuggest'
        params = {
            'type': 'Manga',
            'keyword': keyword,
        }
        resp = _post(url, params=params)

        # Kissmanga returns manga series and links in xml format
        soup = BeautifulSoup(resp.content, 'html.parser')
        atags = soup.find_all('a')
        return [objdict({'name': a.text.strip(),
                         'url': a['href'],
                         'site': self.name}) for a in atags]

    # All kinds of data
    # - name "Naruto"
    # - chapters [{name, url}, {}, ...] - latest first
    # - thumb_url "url"
    # - tags [tag1, tag2, ...]
    # - status "ongoing"/"completed"
    # - descriptions ["paragraph1", "paragraph2", ...]
    # - authors ["Kishimoto Masashi", ...]
    def series_info(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        chapters = self._chapters(soup)
        thumb_url = self._thumbnail_url(soup)
        tags = self._tags(soup)
        name = self._name(soup)
        status = self._status(soup)
        descriptions = self._descriptions(soup)
        authors = self._authors(soup)
        return objdict({
            'site': self.name,
            'chapters': chapters,
            'thumb_url': thumb_url,
            'tags': tags,
            'name': name,
            'status': status,
            'descriptions': descriptions,
            'authors': authors,
        })

    def _chapters(self, soup):
        table = soup.find('table', class_='listing')
        return [objdict({'url': 'http://kissmanga.com' + a['href'],
                         'name': a.string.strip()})
                for a in table.find_all('a')]

    def _thumbnail_url(self, soup):
        return soup.find('link', {'rel': 'image_src'})['href']

    def _tags(self, soup):
        tags = soup.find('span', text='Genres:').find_next_siblings('a')
        return [text.string.strip().lower() for text in tags]

    def _name(self, soup):
        # <link rel='alternate' title='Naruto manga' ...
        # => must remove the ' manga' part
        return soup.find('link', {'rel': 'alternate'})['title'][:-6]

    def _status(self, soup):
        status_span = soup.find('span', {'class': 'info'}, text='Status:')
        return status_span.next_sibling.strip().lower()

    def _descriptions(self, soup):
        desc_span = soup.find('span', {'class': 'info'}, text='Summary:')
        p_tags = desc_span.next_siblings
        desc = [s.text for s in p_tags if type(s) == bs4.element.Tag]
        return desc

    def _authors(self, soup):
        authors = soup.find('span', text='Author:').find_next_siblings('a')
        return [text.string.strip() for text in authors]

    # Chapter data
    # - name "Naruto Ch.101"
    # - pages [url1, url2, ...] - in ascending order
    # - prev_chapter_url
    # - next_chapter_url
    # - series_url
    def chapter_info(self, html):
        pages = self._chapter_pages(html)
        soup = BeautifulSoup(html, 'html.parser')
        name = self._chapter_name(soup)
        series_url = self._chapter_series_url(soup)
        prev, next = self._chapter_prev_next(soup)
        return objdict({
            'name': name,
            'pages': pages,
            'series_url': series_url,
            'next_chapter_url': next,
            'prev_chapter_url': prev,
        })

    def _chapter_prev_next(self, soup):
        next = soup.find('img', class_='btnNext')
        if next is not None:
            next = next.parent['href']
        prev = soup.find('img', class_='btnPrevious')
        if prev is not None:
            prev = prev.parent['href']
        return prev, next

    def _chapter_name(self, soup):
        select = soup.find('select', class_='selectChapter')
        return select.find('option', selected=True).text.strip()

    def _chapter_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        key = get_key(soup)

        pat = re.compile('lstImages\.push\(wrapKA\("(.+?)"\)\);')
        encrypted_urls = pat.findall(html)
        return (decode_url(url, key) for url in encrypted_urls)

    def _chapter_series_url(self, soup):
        a_tag = soup.find('div', id='navsubbar').find('p').find('a')
        return a_tag['href']

    def get_manga_seed_page(self, url):
        return _get(url)

    def get_chapter_seed_page(self, url):
        # http://kissmanga.com/Manga/Manga-Name/Chapter-Name?id=XXXXXXX
        # The "Chapter-Name" part can be any non-empty string and the response
        # will be the same. Problem is that it sometimes contains illegal chars
        # that make pytaku's request fail. Let's replace it with something
        # safe.
        base = url[:url.rfind('/') + 1]  # http://.../Manga-Name/
        id = url[url.rfind('?id='):]  # ?id=XXXXXX
        return _get(base + '_' + id, cookies={'vns_readType1': '1'})

    def search_by_author(self, author):
        url = 'http://kissmanga.com/AuthorArtist/' + author.replace(' ', '-')
        resp = _get(url)

        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('table', class_='listing')

        if table is None:  # no author of this name
            return []

        return [objdict({
            'name': a.text.strip(),
            'url': 'http://kissmanga.com' + a['href'],
            'site': self.name,
        }) for a in table.find_all('a') if len(a['href'].split('/')) == 3]
