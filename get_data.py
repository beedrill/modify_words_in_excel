from bs4 import BeautifulSoup
import urllib.request
import ssl
import certifi
import xlwt
from xlwt import Workbook
website_url = 'https://burningvocabulary.com/blog/hsk-6-vocabulary-list/'
vocabulary_name = 'HSK 6'
output_name = vocabulary_name + '.xls'

fp = urllib.request.urlopen(website_url, context=ssl.create_default_context(cafile=certifi.where()))
mybytes = fp.read()
html_doc = mybytes.decode("utf8")
fp.close()

wb = Workbook()
sheet = wb.add_sheet('vocabulary')
sheet.write(0, 0, 'id')
sheet.write(0, 1, 'word_content')
sheet.write(0, 2, 'pronunciation')
sheet.write(0, 3, 'meaning')
sheet.write(0, 4, 'wordbook')
sheet.write(0, 5, 'part')
sheet.write(0, 6, 'example1')
sheet.write(0, 7, 'example_pronunciation1')
sheet.write(0, 8, 'example_meaning1')
sheet.write(0, 9, 'example2')
sheet.write(0, 10, 'example_pronunciation2')
sheet.write(0, 11, 'example_meaning2')

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.find('table')
trs = table.tbody.find_all('tr')
row = 1
for tr in trs:
    tds = tr.find_all('td')
    print(f'parsing: {tds[0].text}: {tds[1].text}')
    sheet.write(row, 0, tds[0].text)
    sheet.write(row, 1, tds[1].text)
    sheet.write(row, 2, tds[2].text)
    sheet.write(row, 3, tds[3].text)
    sheet.write(row, 4, vocabulary_name)
    row += 1
wb.save(output_name)
    