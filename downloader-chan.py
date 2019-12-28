from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import os

def scrape_links():
    global board_category, url_list, page_title
    url_list_raw = []
    url_list = []

    thread_url = input('Paste the thread URL: ')

    board_category = thread_url.split('/')[-3] + '/'
    page_response = requests.get(thread_url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    page_title = page_content.title.string

    for link in page_content.find_all("a", class_="fileThumb"):
        url_list_raw.append(link.get('href'))

    for url in url_list_raw:
        url = 'https:' + url
        url_list.append(url)

def download_links():
    folder_name = './downloads/' + board_category + str(int(time.time()))
    os.makedirs(folder_name)

    board_folder = './downloads/' + board_category
    with open('./downloads/full_history.txt', 'a+') as full_history:
        full_history.write('"%s" %s\n' % (page_title, folder_name))
    with open(board_folder + '/board_history.txt', 'a+') as board_history:
        board_history.write('"%s" %s\n' % (page_title, folder_name))
    with open(folder_name + '/downloads_list.txt', 'a+') as download_history:
        download_history.write('%s\n' % page_title)
        for url in url_list:
            download_history.write('%s\n' % url)

    print('Thread to download: %s' % page_title)
    for url in url_list:
        filename = folder_name + '/' + url.split('/')[-1]
        print('Downloading ' + url)
        urllib.request.urlretrieve(url, filename)

scrape_links()
download_links()
