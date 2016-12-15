## Author: Rittha
# version 2: add address
import requests
from lxml import html
import re
import string
import pandas as pd
import datetime

topics = []

def process_internal_info(url, event, loc):
    global topics
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ft = tree.xpath('//*[@id="event_info"]')

    try:
        p = ft[0].xpath('./p')
        f = p[0].xpath('./text()[2]')[0].strip()[0:-1].strip()
        t = p[0].xpath('./text()[3]')[0].strip()
        street_where1 = p[1].xpath('./span[2]/span[1]')[0].text_content().strip()
        street_where2 = p[1].xpath('./span[2]/span[2]')[0].text_content().strip()
        street_where3 = p[1].xpath('./span[2]/span[3]')[0].text_content().strip()
        street_where4 = p[1].xpath('./span[2]/span[4]')[0].text_content().strip()
        st_add = street_where1 + " " + street_where2 + " , " + street_where3 + " " + street_where4
        admision = p[2].xpath('./span')[0].text_content().strip()
        category = p[3].xpath('./text()')[0].strip()
        topics.append([event,loc,f,t,admision, st_add, category])
    except:
        pass


def process_thread(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ft = tree.xpath('//*[@id="events"]')
    for ele in ft:
        for post in ele.getchildren():
            title =  post.getchildren()

            try:
                a = title[1].xpath('./h3[1]/a[1]')
                event = a[0].text_content()
                link = a[0].attrib['href']

                p = title[1].xpath('./p')
                loc = p[1].text_content().strip()

                internal_info_url = 'http://www.thebostoncalendar.com' + link
                process_internal_info(internal_info_url, event, loc)
            except:
                pass


numdays = 4
base = datetime.datetime(day=1, month=9, year=2016)
date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
recent_month = 0
for d in reversed(date_list):
    print str(str(d.year) + '-' + str(d.month) + '-' + str(d.day)), 'total events: ' + str(len(topics))
    if recent_month != d.month:
        if len(topics) > 0:
            #new month, just save
            file_name = 'events_' + str(str(d.year) + '-' + str(d.month)) + '.csv'
            print 'saving...' + file_name
            dtopic = pd.DataFrame(topics, columns=['event','location','from','to','admision','address', 'category'])
            dtopic.to_csv('Events/' + file_name, encoding='utf-8')
            topics = []
        recent_month = d.month

    url = "http://www.thebostoncalendar.com/events?day={0}&month={1}&year={2}".format(d.day,d.month,d.year)
    process_thread(url)

if len(topics) > 0:
    #new month, just save
    file_name = 'events_rest.csv'
    print 'saving...' + file_name
    dtopic = pd.DataFrame(topics, columns=['event','location','from','to','admision','address', 'category'])
    dtopic.to_csv('Events/' + file_name, encoding='utf-8')
    topics = []




#page = requests.get(url)
