from bs4 import BeautifulSoup as Soup
from requests import get

ipaddr = '128.107.241.161'

#1 Read from geolocation API (Acquire data)
html = get(f'https://ipapi.co/{ipaddr}').text

#2 Extract coordinate based on the structure of the html
#     (Parse data and convert it into a convenient form)
soup = Soup(html, features='lxml')
locator = soup.find(string='Latitude / Longitude')
if not locator:
    raise Exception(f'Cannot find coordinate for ip {ipaddr}')

coordinate = locator.find_next('td').text

#3 Displaying results (analysis, testing, formatting and outputting)
print(f'IP Address {ipaddr} was found on {coordinate}')
