# Web Crawler for BostonCalendar
Target : http://www.thebostoncalendar.com/


## "event_crawlers.py"
Python web crawler with request, lxml.

Crawler will start from past 1 years to now.
Convert all data into CSV files, columns as following
- event name
- location
- from
- to
- admission
- category
The crawler will save new files every month. (Location Events/)


## "event_data_manipulation.py"
1. Combine all event files in /Events
2. Translate from, to datetime into actual datetime (For pandas)
3. Remove duplicated events
4. Calculate duration of events
5. Convert category from string (with , separators) into categorize features (58 features with 0, 1 value)
