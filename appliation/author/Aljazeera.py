from bs4 import BeautifulSoup
from application.authors.helper import get_page,url_to_open
from datetime import datetime
from application.authors.model import InsertData
import socket
socket.setdefaulttimeout(10)
def scrap_Aljazeera():
    page = get_page('https://www.aljazeera.com/opinion/')
    soup = BeautifulSoup(page, 'html.parser')
    articles= soup.find('div',{'class': 'container container--grid container--white'}).find_all('article')
    print(len(articles))
    for article in articles:
        link ='https://www.aljazeera.com'+ article.find('a',{'class':'author-link'}).get('href')
        page = url_to_open(link)
        print("main link :",link)
        if page is False:
            continue
        else:
            soup = BeautifulSoup(page,'html.parser')
            article_list = soup.find_all('article',{'class':'gc gc--type-opinion gc--list gc--with-image'})
            article_grabber(article_list)
def article_grabber(list_articles):
    print("In Article Grabber ")
    i = 0
    while i < len(list_articles):
        story_link ='https://www.aljazeera.com' + list_articles[i].find('h3', {'class': 'gc__title'}).a.get('href')
        # story_heading = list_articles[i].find('h3', {'class': 'gc__title'}).text
        page = get_page(story_link)
        soup = BeautifulSoup(page, 'html.parser')
        story_heading = soup.find('header', {'class':'article-header'}).find('p').text
        print(story_link, story_heading)
        story_title = soup.find('header', {'class':'article-header'}).find('h1').text
        header = soup.find('div', {'class':'article-info-block opinion-info-block'})
        author_name = header.find('div', {'class':'article-author__name'}).text
        published_date_str = header.find('div', {'class':'article-dates'}).text
        paragraphs = soup.find('div', {'class':'wysiwyg wysiwyg--all-content'}).find_all('p')
        story_content = get_text(paragraphs)
        date = get_Date(published_date_str)
        # print("author_name : "+ author_name)
        # print("Date : ", date)
        # print("story Heading : "+ story_heading)
        # print("story content : "+ story_content)
        value = InsertData(author_name,story_title,story_heading,story_content,date,'Aljazeera')
        print('success')
        if value is True:
            break
        else:
            i = i + 1
def get_Date(date_str):
   date = datetime.strptime(date_str, '%d %b %Y')
   return date
def get_text(paragraphs):
    i = 0
    text = ''
    while i < len(paragraphs):
        text += paragraphs[i].text + ' & '
        i = i+1
    return text
