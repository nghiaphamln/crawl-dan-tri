import requests
from bs4 import BeautifulSoup


def getContent(url):
    data = requests.get(url)
    data = BeautifulSoup(data.content, 'html.parser')
    data = data.find('div', class_='dt-news__body')
    content = data.text
    content = content.replace('\n', ' ').replace('\r', '')
    content = " ".join(content.split())
    return content


def getImage(url):
    imageList = []
    data = requests.get(url)
    data = BeautifulSoup(data.content, 'html.parser')
    image = data.findAll('img')
    for x in range(1, len(image)):
        imageList.append(image[x]['src'])
    return imageList