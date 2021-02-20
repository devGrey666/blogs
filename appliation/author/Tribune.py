from bs4 import BeautifulSoup
from application.authors.helper import get_page
from datetime import datetime
from application.authors.model import InsertData
import socket
timeout = 20
socket.setdefaulttimeout(timeout)
value = False
def scrap_Tribune():
    page = get_page('https://tribune.com.pk/opinion')
    soup = BeautifulSoup(page, 'html.parser')
    opinion_section = soup.find_all('div', {'class': 'opinion-section'})[1]
    anchors = opinion_section.find_all('span', {'class': 'anchorname'})
    # li_tags = opinion_section.find_all('li')
    for anchor in anchors:
        url = anchor.a.get('href')
        htmlPage = get_page(url)
        soup = BeautifulSoup(htmlPage, 'html.parser')
        li_tags = soup.find('ul',{'class': 'tedit-shortnews listing-page'}).find_all_next('div',{'class':'col-md-8'})
        print(len(li_tags))
        for item in li_tags:
            div_tag = item.find('div',{'class':'horiz-news3-caption'})
            if div_tag:
                article_link=div_tag.a.get('href')
                story_title = div_tag.h2.text
                time_span = div_tag.find('span').text
                time_list = time_span.split('|')
                author_name = time_list[0]
                time_string = time_list[1].replace('Updated','')
                time_string = get_time(time_string)
                page = get_page(article_link)
                soup = BeautifulSoup(page,'html.parser')
                main_content = soup.find('div',{'class':'maincontent-customwidth storypage'})
                story_heading = main_content.p.text
                paragraphs = main_content.find('span',{'class':'story-text'}).find_all('p')
                story_content = get_text(paragraphs)
                # print(author_name)
                # print(story_title)
                # print(story_heading)
                # print(story_content)
                # print(time_string)
                value = InsertData(author_name,story_title,story_heading,story_content,time_string,'Tribune')
                if value is True:
                    break
                else:
                    continue
        if value is True:
            continue
    return True
def get_time(timestring):
    try:
        time = datetime.strptime(timestring.strip(),'%b %d, %Y')
    except ValueError as e:
        print("Time string is not correct")
    else:
        return time
def get_text(paragraphs):
    i = 0
    text = ''
    while i < len(paragraphs):
        text += paragraphs[i].text + ' & '
        i = i+1
    return text