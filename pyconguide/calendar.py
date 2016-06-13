import vobject


def generate_ical(presentations):

    cal = vobject.iCalendar()
    cal.add('X-WR-CALNAME').value = 'PyCon 2016'

    for presentation in presentations:

        description = '{}\n\n{}'.format(
            presentation.speakers, presentation.abstract)

        event = cal.add('vevent')
        event.add('summary').value = presentation.title
        event.add('category').value = presentation.category
        event.add('description').value = description
        event.add('dtstart').value = presentation.start_time
        event.add('dtend').value = presentation.end_time
        event.add('location').value = presentation.room or 'TBD'
        event.add('title').value = presentation.url
        event.add('uid').value = 'pycon:2016:presentation:{}'.format(
            presentation.presentation_id)

    return cal.serialize()
