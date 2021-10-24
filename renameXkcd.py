import requests, os
from bs4 import BeautifulSoup

count = 0 # Initialise counter

url = 'https://xkcd.com/' # Defaults to the last page

while True:

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')   # HTML Soup

    comicUrlList = soup.select('#middleContainer > a:nth-child(6)')
    imageUrlList = soup.select('#middleContainer > a:nth-child(8)')

    comicUrl = comicUrlList[0].get('href')
    imageUrl = imageUrlList[0].get('href')

    oldName = os.path.join('xkcd', os.path.basename(imageUrl))
    newName = os.path.join('xkcd', 
                           '{0}-{1}'.format(os.path.basename(comicUrl), 
                           os.path.basename(imageUrl)))

    try:
        os.rename(oldName, newName)
    except FileNotFoundError:
        print(f'{oldName} does not exist')
    else:
        print(f'{oldName} has been renamed')
        count += 1

    if count == 451: break
    else:
        prevLink = soup.select('a[rel="prev"]')[0]
        url = 'https://xkcd.com' + prevLink.get('href')