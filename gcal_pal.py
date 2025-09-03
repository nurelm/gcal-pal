import datetime
import os.path
import yaml
import argparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dateutil import parser

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_color_escape_code(hex_color):
    """
    Converts a hex color to an ANSI escape code for background color.
    """
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f'\033[48;2;{r};{g};{b}m'


def list_calendar_colors(service):
    """
    Lists the available colors for events.
    """
    colors = service.colors().get().execute()
    print("Available Event Colors:")
    for id, color in colors['event'].items():
        hex_code = color['background']
        color_square = get_color_escape_code(hex_code)
        reset_code = '\033[0m'
        print(f"  {color_square}  {reset_code} ID: {id}, Hex: {hex_code}")


def is_event_busy(event, consider_attendees, consider_out_of_office, consider_color_id):
    """
    Determines if an event should be considered busy based on the configured criteria.
    
    Args:
        event: Google Calendar event object
        consider_attendees: Boolean - consider busy if other people are invited
        consider_out_of_office: Boolean - consider busy if event is "Out of Office"
        consider_color_id: String or None - consider busy if event has this color ID
    
    Returns:
        Boolean - True if event should be considered busy
    """
    # Check color criteria (if specified)
    if consider_color_id is not None:
        if event.get('colorId') == str(consider_color_id):
            return True
    
    # Check attendees criteria
    if consider_attendees:
        attendees = event.get('attendees', [])
        # Consider busy if there are other attendees (not just the organizer)
        if len(attendees) > 1:  # More than just the organizer
            return True
        # Also check if there are attendees with different email than organizer
        organizer_email = event.get('organizer', {}).get('email', '')
        for attendee in attendees:
            if attendee.get('email') != organizer_email:
                return True
    
    # Check "Out of Office" criteria
    if consider_out_of_office:
        # Check if event is marked as "Out of Office" in various ways
        event_type = event.get('eventType', '')
        if event_type == 'outOfOffice':
            return True
        
        # Also check the event title for common OOO indicators
        title = event.get('summary', '').lower()
        ooo_keywords = ['out of office', 'ooo', 'vacation', 'sick', 'personal', 'away']
        if any(keyword in title for keyword in ooo_keywords):
            return True
    
    return False


def main():
    """
    Finds available time slots in the user's Google Calendar.
    """
    arg_parser = argparse.ArgumentParser(description='Find available time in your Google Calendar.')
    arg_parser.add_argument('--start-date', help='Start date in YYYY-MM-DD format. Defaults to the beginning of next week.')
    arg_parser.add_argument('--end-date', help='End date in YYYY-MM-DD format. Defaults to the end of next week.')
    arg_parser.add_argument('--list-colors', action='store_true', help='List available calendar colors and exit.')
    args = arg_parser.parse_args()

    service = get_calendar_service()

    if args.list_colors:
        list_calendar_colors(service)
        return

    # Load configuration
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Now you can access the configuration values like this:
    min_duration = config['min_duration']
    working_hours_start = config['working_hours']['start']
    working_hours_end = config['working_hours']['end']
    
    # Load busy criteria configuration with defaults
    busy_criteria = config.get('busy_criteria', {})
    consider_attendees = busy_criteria.get('consider_attendees', True)
    consider_out_of_office = busy_criteria.get('consider_out_of_office', True)
    consider_color_id = busy_criteria.get('consider_color_id')

    print("Successfully connected to Google Calendar API.")
    print(f"Minimum meeting duration: {min_duration} minutes")
    print("Busy criteria:")
    print(f"  - Consider attendees: {consider_attendees}")
    print(f"  - Consider out of office: {consider_out_of_office}")
    if consider_color_id is not None:
        print(f"  - Consider color ID: {consider_color_id}")
    else:
        print("  - Color criteria: disabled")
    print()

    # Get the start and end dates
    if args.start_date:
        start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
    else:
        now = datetime.datetime.utcnow()
        start_date = now + datetime.timedelta(days=(7 - now.weekday()))
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    if args.end_date:
        end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
    else:
        end_date = start_date + datetime.timedelta(days=5)


    # Fetch events from the primary calendar
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date.isoformat() + 'Z',
        timeMax=end_date.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # Fetch events from the holiday calendar
    if config.get('holiday_calendar_id'):
        holiday_events_result = service.events().list(
            calendarId=config['holiday_calendar_id'],
            timeMin=start_date.isoformat() + 'Z',
            timeMax=end_date.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        holiday_events = holiday_events_result.get('items', [])
        events.extend(holiday_events)

    # Separate all-day events from timed events
    holiday_dates = []
    if config.get('holiday_calendar_id'):
        for event in holiday_events:
            if 'date' in event['start']:
                holiday_dates.append(datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d').date())

    timed_events = []
    for event in events:
        if 'dateTime' in event['start']:
            # Use the new busy detection logic
            if is_event_busy(event, consider_attendees, consider_out_of_office, consider_color_id):
                start = parser.parse(event['start']['dateTime']).astimezone()
                end = parser.parse(event['end']['dateTime']).astimezone()
                timed_events.append((start, end))

    # Combine all busy times
    busy_times = timed_events

    # Add manual holidays to busy times
    if config.get('holidays'):
        for holiday in config['holidays']:
            holiday_date = datetime.datetime.strptime(holiday, '%Y-%m-%d').date()
            busy_times.append(
                (
                    datetime.datetime.combine(holiday_date, datetime.time.min).astimezone(),
                    datetime.datetime.combine(holiday_date, datetime.time.max).astimezone()
                )
            )

    # Sort busy times
    busy_times.sort()

    # Find available slots
    available_slots = []
    num_days = (end_date - start_date).days
    for day_offset in range(num_days + 1):
        day = start_date + datetime.timedelta(days=day_offset)

        # Skip holidays
        if day.date() in holiday_dates:
            continue
        
        # Get working hours for the day
        working_start = day.replace(
            hour=int(working_hours_start.split(':')[0]),
            minute=int(working_hours_start.split(':')[1])
        ).astimezone()
        working_end = day.replace(
            hour=int(working_hours_end.split(':')[0]),
            minute=int(working_hours_end.split(':')[1])
        ).astimezone()

        # Get lunch break for the day
        lunch_start_time = config['lunch_break']['start']
        lunch_end_time = config['lunch_break']['end']
        lunch_start = day.replace(
            hour=int(lunch_start_time.split(':')[0]),
            minute=int(lunch_start_time.split(':')[1])
        ).astimezone()
        lunch_end = day.replace(
            hour=int(lunch_end_time.split(':')[0]),
            minute=int(lunch_end_time.split(':')[1])
        ).astimezone()

        # Combine all busy times for the day
        day_busy_times = [(lunch_start, lunch_end)]
        for start, end in busy_times:
            if start.date() == day.date() or end.date() == day.date():
                day_busy_times.append((start, end))
        
        day_busy_times.sort()

        # Find free slots
        current_time = working_start
        for start, end in day_busy_times:
            if current_time < start:
                if (start - current_time).total_seconds() / 60 >= min_duration:
                    available_slots.append((current_time, start))
            current_time = max(current_time, end)

        if current_time < working_end:
            if (working_end - current_time).total_seconds() / 60 >= min_duration:
                available_slots.append((current_time, working_end))

    slots_by_day = {}
    for start, end in available_slots:
        day = start.strftime('%A, %-m/%-d')
        if day not in slots_by_day:
            slots_by_day[day] = []
        slots_by_day[day].append((start, end))

    for day, slots in slots_by_day.items():
        print(f"{day}:")
        for start, end in slots:
            print(f"{start.strftime('%-I:%M%p').lower()} - {end.strftime('%-I:%M%p').lower()}")
        print()


if __name__ == '__main__':
    main()
