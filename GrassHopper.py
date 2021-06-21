from bs4 import BeautifulSoup
import requests
import re
import openpyxl
from openpyxl import Workbook


# Open excel file
book = openpyxl.open('excel_file.xlsx', read_only=True)
sheet = book.active
# Get donor and clear it from 'https' and slashes
acceptor_domain = sheet['A1'].value
acceptor_domain = str(acceptor_domain).replace('https:', '').replace('/', '')
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
           'accept': '*/*'}
#Variables lists
donor_list = [] # List of donor URL`s
# Result list
result_list = []
# Title list
title_list = ['URL', 'Status code', 'Sponsored', 'NoFollow', 'UGC', 'Links Status']

# Get all donors URL from the excel list
for row in range(1,sheet.max_row+1):
    url_list = sheet[row][1].value
    if url_list != None:
        donor_list.append(url_list)


def get_response_code(code):
    try:
        r = requests.get(code, headers=HEADERS)
        return r.status_code
    except requests.exceptions.RequestException as error:
        return 'Error'


def get_html(url):
    r = requests.get(url, headers=HEADERS, allow_redirects=False)
    return r.text

def get_ahref(html, url_donora, code):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(href=re.compile(acceptor_domain))
    items = str(items).split()
    ahrefs_list = ['','','','','', '']
    if len(items) != 1:
        ahrefs_list[-1] = 'Found'
    else:
        ahrefs_list[-1] = 'Not Found'
    if code == 200:
        for x in items:
            if 'href' in x:
                ahrefs_list[0] = url_donora
            if 'href' in x:
                ahrefs_list[1] = code
            if 'sponsored' in x:
                ahrefs_list[2] = 'Sponsored'
            if 'nofollow' in x:
                ahrefs_list[3] = 'Nofollow'
            if 'ugc' in x:
                ahrefs_list[4] = 'UGC'
        else:
            ahrefs_list[0] = url_donora
            ahrefs_list[1] = str(code)
        #print(ahrefs_list)
        result_list.append(ahrefs_list)
    else:
        ahrefs_list[0] = url_donora
        ahrefs_list[1] = str(code)
        result_list.append(ahrefs_list)


for x in donor_list:
    code = get_response_code(x)
    if code != 200:
        code_error = [x,code]
        result_list.append(code_error)
    else:
        html = get_html(x)
        get_ahref(html, x, code)


result_book = Workbook()
result_book_sheet = result_book.active
result_book_sheet.append(title_list)

for row in result_list:
    result_book_sheet.append(row)

result_book.save('Result_list.xlsx')

if '__main__' == __name__:
    print('Success')