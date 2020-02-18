
# import BeautifulSoup.
# import csv library
# import http request library.

from bs4 import BeautifulSoup
import csv
import requests

page = requests.get("https://hr.uw.edu/professional-staff-program/#appendix-professional-staff-salaries")

# status code 200 means we access the web page successfully.
print(page.status_code)

# save raw, unprocessed data to a variable.
raw = page.content

# print out the content to visually inspect.
# print(raw)

soup = BeautifulSoup(raw, 'html.parser')

# our target is the "Research Scientist/Engineer Monthly and Annual Salaries".
# after visually inspecting the html source, we know that there is 4 tables,
# and our target is the 4th table.

# print out the table to visually inspect and verify.
# print(soup.select('table:nth-of-type(4)'))

# th
row_head = []

# td
row_data = []

for t1 in soup.select('table:nth-of-type(4)'):
    for th in t1.find_all('th'):
        row_head.append(th.get_text())
    for td in t1.find_all('td'):
        row_data.append(td.get_text())

# function replaces an empty character with a newline character to the list
def newline(lst):
    c = 0
    for x in lst:
        if x == '':
            lst[c] = '\n'
        c = c + 1


newline(row_head)
newline(row_data)

# adding, removing, swapping elements to compensate padding spaces in html
row_head.insert(4, row_head[0])
row_head.remove(row_head[0])
row_head.insert(1, '')
row_head.insert(0, '')
row_head.insert(0, '')

# writing processed data to a csv file
with open('uw_paygrade.csv', 'w', encoding='utf-8', newline='\n') as pg:
    pgwriter = csv.writer(pg, delimiter =',', dialect='excel', lineterminator='\r')
    temp = []
    for x in row_head:
        if x == '\n':
            pgwriter.writerow(temp)
            temp = []
        else:
            temp.append(x)
    for x in row_data:
        if x == '\n':
            pgwriter.writerow(temp)
            temp = []
        else:
            temp.append(x)
