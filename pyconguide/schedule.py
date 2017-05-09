import datetime
import re
import time

import requests
from django_rq import job
from lxml import etree
from pytz import timezone

from .models import Presentation, PyCon


BASE_URL = 'https://us.pycon.org{}'
SCHEDULE_URL = BASE_URL.format('/2017/schedule/talks/')
PRESENTATION_RE = re.compile(r'(/2017/schedule/presentation/(\d+)/)')
SESSION_RE = re.compile(r'(/2017/schedule/session/(\d+)/)')
DATES = {
    'Friday': datetime.date(2017, 5, 19),
    'Saturday': datetime.date(2017, 5, 20),
    'Sunday': datetime.date(2017, 5, 21),
}


http = requests.Session()
http.headers = {
    'User-Agent': 'pyconguide-bot',
}

pacific = timezone('America/Los_Angeles')


def parse_time(s):
    s = s.strip().replace('.', '').upper()
    if s == 'NOON':
        return datetime.time(12, 0, 0, 0)
    try:
        dt = datetime.datetime.strptime(s, '%I:%M %p')
    except ValueError:
        dt = datetime.datetime.strptime(s, '%I %p')
        dt = dt.replace(minute=0)
    return dt.time()


@job
def scrape_pycon():

    resp = http.get(SCHEDULE_URL)
    matchiter = PRESENTATION_RE.finditer(resp.text)
    presentation_ids = [int(m.groups()[1]) for m in matchiter]

    current_ids = Presentation.objects.values_list(
        'presentation_id', flat=True)

    to_remove = set(current_ids) - set(presentation_ids)
    Presentation.objects.filter(presentation_id__in=to_remove).delete()

    for presentation_id in presentation_ids:
        # scrape_presentation.delay(presentation_id)
        try:
            scrape_presentation(presentation_id)
        except etree.XMLSyntaxError:
            print(f'!!! Unable to parse presentation {presentation_id}')


    # collect session_id

    matchiter = SESSION_RE.finditer(resp.text)
    session_ids = sorted(set(int(m.groups()[1]) for m in matchiter))

    for session_id in session_ids:
        #scrape_session.delay(session_id)
        try:
            scrape_session(session_id)
        except etree.XMLSyntaxError:
            print(f'!!! Unable to parse session {session_id}')


@job
def scrape_presentation(presentation_id):

    url = BASE_URL.format(
        '/2017/schedule/presentation/{}/'.format(presentation_id))

    print(f'scraping presentation {url}')

    defaults = {
        'pycon': PyCon.objects.get(year=2017),
        'url': url,
    }

    # fetch and parse

    resp = requests.get(url)
    parser = etree.HTMLParser()

    doc = etree.fromstring(resp.text, parser)

    elems = doc.cssselect('.box-content h2')
    defaults['title'] = elems[0].text.strip()

    elems = doc.cssselect('.box-content h4')
    day, start_end = elems[0].text.strip().split('\n')
    start, end = start_end.split('–')

    date = DATES.get(day)
    defaults['start_time'] = pacific.localize(
        datetime.datetime.combine(date, parse_time(start)))
    defaults['end_time'] = pacific.localize(
        datetime.datetime.combine(date, parse_time(end)))

    elems = doc.cssselect('.box-content h4 a')
    names = []
    for elem in elems:
        names.append(elem.text)
    defaults['speakers'] = ', '.join(names)

    elems = doc.cssselect('.box-content .dl-horizontal dd')
    if elems:
        defaults['audience'] = elems[0].text.strip()
        defaults['category'] = elems[1].text.strip()

    elems = doc.cssselect('.box-content .description')
    defaults['description'] = elems[0].text.strip()

    elems = doc.cssselect('.box-content .abstract')
    if elems:
        defaults['abstract'] = elems[0].text.strip()

    Presentation.objects.update_or_create(
        presentation_id=presentation_id, defaults=defaults)

    time.sleep(0.2)


@job
def scrape_session(session_id):

    pycon = PyCon.objects.get(year=2017)

    url = BASE_URL.format(
        '/2017/schedule/session/{}/'.format(session_id))

    print(f'scraping session {url}')

    resp = requests.get(url)
    parser = etree.HTMLParser()
    doc = etree.fromstring(resp.text, parser)

    elems = doc.cssselect('.table a')
    presentations = []
    for p in elems:
        if p.text is not None:
            presentations.append(p.text[1:5])

    elems = doc.cssselect('.table tr td')
    rooms = []
    preamble = "talk in "
    for r in elems:
        if r.text is not None:
            i = r.text.find(preamble) + len(preamble)
            rooms.append(r.text[i:].replace('Ballroom ', ''))

    for presentation_id, room in zip(presentations, rooms):
        params = {
            'presentation_id': presentation_id,
            'room': room
        }
        Presentation.objects.filter(
            presentation_id=presentation_id, pycon=pycon
        ).update(**params)
