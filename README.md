# 📅 Google Calendar Time Finder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> Find open time slots in your Google Calendar, so you can easily answer the question "When are you free to talk next week?"

A smart calendar availability finder that connects to your Google Calendar and intelligently identifies available time slots based on your working hours, lunch breaks, holidays, and customizable busy criteria. Perfect for scheduling meetings, finding focus time, or answering availability questions quickly.

**Built with ❤️ by [NuRelm](https://nurelm.com)**

## Features

-   Finds available time slots in any date range.
-   Defaults to finding time in the next week.
-   Considers your working hours and a daily lunch break.
-   Respects holidays from a specified Google Calendar (e.g., your company's holiday calendar) and a manual list of dates.
-   Intelligent busy detection with configurable criteria:
    -   Events with other attendees (meetings with colleagues)
    -   "Out of Office" events (vacation, sick days, etc.)
    -   Events of a specific color (for custom busy indicators)

## Setup

### 1. Enable the Google Calendar API

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project (or select an existing one).
3.  In the navigation menu, go to **APIs & Services > Library**.
4.  Search for "Google Calendar API" and click **Enable**.

### 2. Create Credentials

1.  In the navigation menu, go to **APIs & Services > Credentials**.
2.  Click **Create Credentials** and choose **OAuth client ID**.
3.  If prompted, configure the consent screen. For the user type, select **External** and click **Create**.
4.  On the next screen, provide an app name (e.g., "Calendar Time Finder") and your email address. You can leave the other fields blank.
5.  For the application type, select **Desktop app** and click **Create**.
6.  A window will pop up with your client ID and client secret. Click the **Download JSON** button to download the credentials file.
7.  Rename the downloaded file to `credentials.json` and place it in the same directory as the script.

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Finding Available Time

To find available time in the next week, simply run the script:

```bash
python gcal_pal.py
```

### Listing Available Colors

To list the available calendar colors, use the `--list-colors` argument:

```bash
python gcal_pal.py --list-colors
```

This will output a list of color IDs, their hex codes, and their English names. You can use these IDs to configure the `busy_criteria.consider_color_id` setting.

To find available time in a specific date range, use the `--start` and `--end` arguments:

```bash
python gcal_pal.py --start-date 2025-09-01 --end-date 2025-09-05
```

The first time you run the script, it will open a browser window to ask for permission to access your Google Calendar. After you grant permission, it will store the authorization token in a `token.json` file for future use.

### Example Output

```
Successfully connected to Google Calendar API.
Minimum meeting duration: 60 minutes
Busy criteria:
  - Consider attendees: true
  - Consider out of office: true
  - Consider color ID: 5

Available slots:
Monday, 8/25:
10:30am - 11:30am
2:00pm - 5:00pm

Tuesday, 8/26:
9:30am - 10:30am
12:30pm - 2:00pm
3:00pm - 5:00pm

...
```

## Configuration

The `config.yaml` file allows you to customize the script's behavior.

| Setting               | Description                                                                                                                               | Example                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `min_duration`        | The minimum duration for a meeting in minutes.                                                                                            | `60`                                                    |
| `working_hours`       | Your working hours.                                                                                                                       | `start: "09:00"`<br>`end: "17:00"`                      |
| `lunch_break`         | The time to block out for lunch.                                                                                                          | `start: "12:00"`<br>`end: "13:00"`                      |
| `holidays`            | A list of manual holiday dates in YYYY-MM-DD format.                                                                                      | `["2025-12-25"]`                                        |
| `holiday_calendar_id` | The ID of a Google Calendar for holidays.                                                                                                 | `'en.usa#holiday@group.v.calendar.google.com'`          |
| `busy_criteria`       | Configuration for determining which events should be considered busy.                                                                     | See below                                               |
| `busy_criteria.consider_attendees` | If true, events with other attendees will be considered busy (default: true).                                              | `true`                                                  |
| `busy_criteria.consider_out_of_office` | If true, "Out of Office" events will be considered busy (default: true).                                              | `true`                                                  |
| `busy_criteria.consider_color_id` | If set, only events with this color ID will be considered busy. You can use the `--list-colors` command to find available color IDs. | `5`                                                     |

## 🛠️ Development

### Prerequisites

- Python 3.8 or higher
- Google Calendar API access
- A Google account with calendar data

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/gcal-pal.git
cd gcal-pal
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Follow the setup instructions above to configure Google Calendar API access.

### Running Tests

```bash
python -m pytest tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About NuRelm

This project is maintained by [NuRelm](https://nurelm.com), a software development company that builds innovative solutions for businesses. We're passionate about creating tools that make developers' and users' lives easier.

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/your-username/gcal-pal/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/your-username/gcal-pal/issues)
- 📧 **Email**: support@nurelm.com
- 🌐 **Website**: [nurelm.com](https://nurelm.com)

## 🙏 Acknowledgments

- Google Calendar API team for providing excellent documentation
- The Python community for amazing libraries
- All contributors who help make this project better

---

<p align="center">
  Made with ❤️ by <a href="https://nurelm.com">NuRelm</a>
</p>
