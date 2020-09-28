import os
import re
import sys
import urllib3
import argparse
import requests
import urllib.parse
import urllib.request
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.exceptions import RequestException


def arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Download PDF files from web directory.')
    parser.add_argument('-u', '--url', type=str, help='URL of web directory.')
    parser.add_argument('-d', '--dir', type=str, help='Directory of user PC.')
    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="Verbose mode.")
    args = parser.parse_args()
    return args


def getAllUrl(url):
    try:
        http = urllib3.PoolManager()
        page = http.request('GET', url)
    except:
        return []
    urlList = []
    soup = BeautifulSoup(page.data, 'html.parser')
    soup.prettify()
    for anchor in soup.findAll('a', href=True):
        if not 'http://' in anchor['href']:
            if urllib.parse.urljoin(url, anchor['href']) not in urlList:
                urlList.append(urllib.parse.urljoin(url, anchor['href']))
        else:
            if anchor['href'] not in urlList:
                urlList.append(anchor['href'])
    return urlList


def listAllUrl(URL):
    urls_tmp = getAllUrl(URL)
    urls = []
    for y in urls_tmp:
        urls.append(y)
    return urls


def download_files(local_dir, url_list):
    for i in url_list:
        a = urlparse(i)
        filename = os.path.basename(a.path)
        urllib.request.urlretrieve(i, local_dir + '\\' + filename)


def get_dir_name(DIR, URL):
    fullname = os.path.join(DIR, URL)
    path, basename = os.path.split(fullname)
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    options = arguments(sys.argv[1:])
    if options.verbose:
        print("Verbose mode on")
    else:
        print("Verbose mode off")
    URL = options.url
    DIR = options.dir
    print('Download from web directory: ' + URL + '\nStore files at local (User) directory: ' + DIR)
    Path(DIR).mkdir(parents=True, exist_ok=True)
    url_list = listAllUrl(URL)
    url_list = list(filter(lambda k: 'pdf' in k, url_list))
    print('PDF files found at: ')
    pprint(url_list)
    print('Starting downloading sequence ...')
    download_files(DIR, url_list)
    if(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) == len(url_list)):
        print('All files were downloaded successfully.')
    else:
        print('Single or multiple failures were occured.')
    text_file = open(DIR + "\\url.txt", "w")
    text_file.write(URL)
    text_file.close()


if __name__ == '__main__':
    main()
