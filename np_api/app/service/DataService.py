from icalendar import Calendar
import os

from model.Event import Event
from model.PeriodEnum import PeriodEnum
from dto.EventDto import EventDto


def group_by_date(events, days_necessary):
    grouped_events = {}
    d_current_day = None
    day_count = 0

    for event in events:
        date_event = event.d_start.isoformat()

        if d_current_day != date_event:
            day_count += 1
            if day_count > days_necessary:
                break

            d_current_day = date_event
            grouped_events[d_current_day] = []

        current_day_schedule = grouped_events.get(d_current_day)
        current_day_schedule.append(event)
        grouped_events[d_current_day] = current_day_schedule

    return grouped_events


def prepare_schedule_dto(schedule):
    schedule_dto = {}

    for day in schedule.keys():
        events = []

        for event in schedule[day]:
            events.append(EventDto(event.lecture, event.t_start, event.t_end).to_dict())

        schedule_dto[day] = events

    return schedule_dto


def get_schedule_data(period):
    events = get_events()

    if events:
        schedule = group_by_date(events, PeriodEnum(int(period)).days)
        schedule_dto = prepare_schedule_dto(schedule)

        return schedule_dto
    else:
        return []


def get_events():
    # Open ics calendar file
    # ics file should be in the same location as this script
    # local environment path
    # data_file_path = os.path.join(os.path.dirname(__file__) + "\..\\resources", "studijas.ics")
    data_file_path = "/usr/src/app/resources/studijas.ics"
    ics_file = open(data_file_path, 'rb')
    calendar = Calendar.from_ical(ics_file.read())

    events = []
    # Get all events
    for component in calendar.walk():
        if component.name == "VEVENT":
            # Get properties of a single calendar event
            summary = component.get("summary")
            dt_start = component.get("dtstart").dt
            dt_end = component.get("dtend").dt

            d_start = dt_start.date()
            d_end = dt_end.date()

            t_start = dt_start.time().strftime('%H:%M')
            t_end = dt_end.time().strftime('%H:%M')

            event = Event(summary, d_start, t_start, d_end, t_end)
            events.append(event)

    # Close ics file
    ics_file.close()
    return events
