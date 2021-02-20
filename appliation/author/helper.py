from bs4 import BeautifulSoup
from application.authors.model import InsertData
from urllib.request import Request, urlopen, FancyURLopener
from urllib.error import URLError
import time
import socket
from datetime import datetime
# Setting default time out to 10 seconds otherwise its not defined to fetch pages
timeout = 20
socket.setdefaulttimeout(timeout)
value = False
def scrap_Dawn():
    urls = "https://www.dawn.com/opinion"
    page = url_to_open(urls)
    soup = BeautifulSoup(page, 'html.parser')
    div_articles = soup.find_all('div', {'class': 'w-full'})[5]
    articles = div_articles.find_all('article')
    time.sleep(2)
    for article in articles:
        story_byline = article.find('span', {'class': 'story__byline'})
        author_name = story_byline.text
        author_blogs_link = story_byline.a.get('href')
        blogger_page = url_to_open(author_blogs_link)
        if blogger_page is False:
            continue
        soup = BeautifulSoup(blogger_page, 'html.parser')
        div_wrapper = soup.find('div', {'class': 'mr-4 m-2'})
        articles = div_wrapper.find_all('article')
        for article in articles:
            story_title = article.find('h2', {'class': 'story__title'})
            story_heading = article.find('div', {'class': 'story__excerpt'})
            story_time_span = story_heading.find("span",{"class": 'timestamp--time'}).get('title')
            timestamp = get_time_stamp(story_time_span)
            blog_link = story_title.a.get('href')
            blog_page = url_to_open(blog_link)
            if blog_page is False:
                continue
            soup = BeautifulSoup(blog_page, 'html.parser')
            div_story_content = soup.find('div', {'class': 'story__content'}).find_all('p')
            story_heading_text = div_story_content[0].text
            paragraph_text = get_text(div_story_content)
            # print(story_time_span)
            # print(type(story_time_span))
            # print(paragraph_text)
            # print(author_name)
            # print(story_title.text)
            # print(story_heading.text)
            value = InsertData(author_name, story_title.text, story_heading_text, paragraph_text, timestamp, 'Dawn')
            if value is True:
                break
        if value is True:
            break
    return True

def get_text(content):
    text = ''
    i = 1
    while i < (len(content)-2):
      if content[i].text is not None:
        text += content[i].text + ' & '
        i = i+1
      else:
          continue
    return text

def url_to_open(url):
    req = Request(url=url, headers={'User_Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
    except URLError as e:
        #     Following code handles URLError
        if hasattr(e, 'reason'):
            print("Sorry!!! Server is not reachable")
            print('Reason : ', e.reason)
        #     Following code handles HTTPError
        elif hasattr(e, 'code'):
            print("This request can not be fulfilled by Server")
            print("Error Code : ", e.code)
    else:
        page = response.read()
        if page:
         return page
        else:
            return False
def get_time_stamp(time_str):
    timestamp = datetime.fromisoformat(time_str)
    return timestamp
# blog_scraper()
# time_string = '2021-01-29T06:36:23+05:00'
# d = datetime.fromisoformat(time_string)
# date = d.strftime("%d/%m/%Y  %H:%M")
# datelocal = d.strftime("%b %d %Y")
# datelocal2 = d.strftime(" %d %B, %Y")
# timelocal = d.strftime("%H:%M %p")
# print("Format can be like this : "+date)
# print("Format can be like this : "+datelocal)
# print("Format can be like this : "+datelocal2)
# print("Format can be like this : "+timelocal)
# now = datetime.now()
# timelcoalnow = now.strftime("%I:%M %p")
#
# print("Format can be like this : "+timelcoalnow)
class OpenURL(FancyURLopener):
    version = "Mozilla/5.0"
def get_page(url):
    fancy_opener = OpenURL()
    try:
        page = fancy_opener.open(url)
    except TimeoutError:
        print("Timed Out")
    except ConnectionError:
        print("Connection Error")
    else:
        return page