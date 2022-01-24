from bs4 import BeautifulSoup
import requests
import re
import openpyxl
from openpyxl import Workbook
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
           'accept': '*/*'}

COLUMN_TITLES = ['URL', 'Status code', 'Sponsored', 'NoFollow', 'UGC', 'Links Status']


def openExcel():
    open_book = openpyxl.open('excel_file.xlsx', read_only=True)
    sheet = open_book.active
    url_list = [x[1] for x in sheet.values]
    acceptor_domain = str(sheet['A1'].value).replace('https:', '').replace('/', '')
    return acceptor_domain, url_list

def checkLinkAttrs(href):
    links_attrs = [None, None, None]
    if 'ugc' in href:
        links_attrs[0] = 'Found'
    if 'sponsored' in href:
        links_attrs[1] = 'Found'
    if 'nofollow' in href:
        links_attrs[2] = 'Found'
    return links_attrs

def formatResult(links_attrs, url, status_code):
    format_result = [url, status_code]
    format_result.extend(links_attrs)
    format_result.append('Links found')
    return format_result

def getPageData(url_list, acceptor_domain):
    result = []
    for url in url_list:
        page = requests.get(url, headers=HEADERS, allow_redirects=False)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            hrefs = str(soup.find_all(href=re.compile(acceptor_domain)))
            if len(hrefs) > 2:
                links_attrs = checkLinkAttrs(hrefs)
                format_result = formatResult(links_attrs, url, page.status_code)
                result.append(format_result)
            else:
                no_links = [url, page.status_code, None, None, None, 'Links not found']
                result.append(no_links)
        else:
            not_200 = [url, page.status_code, None, None, None, 'Page unavailable']
            result.append(not_200)
    return result

def createResultFile(result_list):
    result_book = Workbook()
    result_book_sheet = result_book.active
    result_book_sheet.append(COLUMN_TITLES)
    for row in result_list:
        result_book_sheet.append(row)

    result_book.save('Result_list.xlsx')


acceptor_domain, url_list = openExcel()
result_list = getPageData(url_list, acceptor_domain)
createResultFile(result_list)
