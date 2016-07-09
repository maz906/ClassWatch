from bs4 import BeautifulSoup
from urllib.request import urlopen

def createsoup(url):
    try:
        return BeautifulSoup(urlopen(url).read(), 'html.parser')
    except URLError as u:
        print('Error in doing stuff. Needs further development. Should validate before this.')
        raise e

