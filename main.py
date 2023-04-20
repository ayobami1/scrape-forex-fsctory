import itertools

import cloudscraper
from bs4 import BeautifulSoup
import datetime

url = 'https://www.forexfactory.com/calendar?day=today'


#
# for row, row_ in itertools.zip_longest(rows, rows_2, fillvalue=0):
#
#     try:
#         time_str = row.find('td', {'class': 'calendar__cell calendar__time time'}).div.text.strip()
#         time_est = datetime.datetime.strptime(time_str, '%I:%M%p').replace(tzinfo=est_tz)
#         time_cet = time_est.astimezone(cet_tz).strftime('%I:%M%p')
#
#         # print(time)
#     except:
#         time_str = row_.find('span', {'class': 'upnext'}).text.strip()
#         time_est = datetime.datetime.strptime(time_str, '%I:%M%p').replace(
#             tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
#         time_cet = time_est.astimezone(datetime.timezone(datetime.timedelta(hours=1))).strftime('%I:%M%p')
#
#
#
#     # day = day_span.span.text
#     #
#     # print(day)
#     try:
#         impact = row.find('td', {'class': 'calendar__impact'}).span['title']#.split()[0].lower()
#     except AttributeError:
#         impact = ''
#     # print(impact)
#     try:
#         currency = row.find('td', {'class': 'calendar__currency'}).text.strip()
#     except:
#         currency = row_.find('td', {'class': 'calendar__currency'}).text.strip()
#
#     news = row.find('td', {'class': 'calendar__event'}).span.text.strip()
#     # print(currency, news)
#     try:
#         actual = row.find('td', {'class': 'calendar__actual'}).span.text.strip()
#         # print(actual)
#     except AttributeError:
#         actual = ''
#     try:
#         forecast = row.find('td', {'class': 'calendar__forecast'}).span.text.strip()
#         # print(forecast)
#     except AttributeError:
#         forecast = ''
#     try:
#         previous = row.find('td', {'class': 'calendar__previous'}).span.text.strip()
#         # print(previous)
#     except AttributeError:
#         previous = ''
#     #
#     print(
#         f"\nCurrency: {currency}\nTime: {time_cet}\nImpact: {impact}\nNews: {news}\n")#\nActual: {actual}\nForecast: {forecast}\nPrevious: {previous}\n")
#


def get_today_news():
    scraper = cloudscraper.create_scraper()
    try:
      response = scraper.get(url)
    except Exception as e:
        print(str(e))

    print(response.status_code)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.find_all('tr', {'class': 'calendar__row calendar_row calendar__row--grey'})
        # rows_2  = soup.find_all('tr', {'class': 'calendar__row calendar_row'})
        # print(rows)
        day_span = soup.find('span', {'class': 'date'}).find('span')
        print("Today is  :", day_span.text,"GMT+ 0")

        # Convert timezone from EST to CET
        est_tz = datetime.timezone(datetime.timedelta(hours=-5))
        cet_tz = datetime.timezone(datetime.timedelta(hours=-1))

        status_code = response.status_code
        print("\n"*2, "*"*50)
        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.find_all('tr', class_='calendar__row')

        recent = []
        loop = 0
        for row in rows:
            # Extract the time
            try:
             time = row.select_one('.calendar__time div')
             if time is None:
                 continue
             time = time.get_text(strip=True)
             time = datetime.datetime.strptime(time, '%I:%M%p').replace(tzinfo=est_tz)
             time = time.astimezone(cet_tz).strftime('%I:%M%p')

             if len(recent) > 1:
                 if recent[-1] == "PM" and time[5:]=="AM": # and last_time =="AM":
                     break

            except:
                time =''

            # Extract the currency
            currency = row.select_one('.calendar__currency').get_text(strip=True)

            # Extract the impact
            impact = row.select_one('.calendar__impact-icon img')['alt']
            impact = row.find('td', {'class': 'calendar__impact'}).span['title']

            # Extract the news
            news = row.select_one('.calendar__event-title').get_text(strip=True)

            print(f"\nTime: {time}")
            print(f"Currency: {currency}")
            print(f"Impact: {impact}")
            print(f"News: {news}\n")
            if time != '':
                recent.append(time[5:])
        return status_code
    except:
        return 403


while 1:#  response.status_code !=200:

   code =  get_today_news()

   if code !=200:
       continue
   else:
       break

   # break
