import requests
from bs4 import BeautifulSoup
from module.content import getContent, getImage
from module.deletestopword import removeStopWord
from module.database import insertToDataBase


def getNews(url, db, category):
    data = requests.get(url)
    data = BeautifulSoup(data.content, 'html.parser')
    a = data.findAll('a', class_='news-item__sapo')
    for x in a:
        key = {'Title': x.attrs['title']}
        value = {
            '$set': {
                'Title': x.attrs['title'],
                'Link': 'https://dantri.com.vn' + x.attrs['href'],
                'Quote': x.text,
                'Image': getImage('https://dantri.com.vn' + x.attrs['href']),
                'Category': category,
                'Content': getContent('https://dantri.com.vn' + x.attrs['href'])
            }
        }
        insertToDataBase(key, value, db)
