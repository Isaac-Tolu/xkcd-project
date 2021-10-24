"""
    Downloads the next 10 XKCD comics.
    It works in descending order.
"""

import requests, os
from bs4 import BeautifulSoup

# List containing all the files in the xkcd directory
# REVISE: Get the first and last files without using os.listdir()
dirList = os.listdir('./xkcd/')

lastImageNum = dirList[0].split('-')[0]

url = 'https://xkcd.com/' + f'{int(lastImageNum) - 1}'

count = 0

while not url.endswith('#'):
    
    # Download the page 
    print(f'Downloading page: {url}')
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')  # HTML soup

    # Find the comic image
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'https:' + comicElem[0].get('src')

    #Download the image.
    print(f'Downloading image: {comicUrl}')
    res = requests.get(comicUrl)
    res.raise_for_status()

    # Save the image to ./xkcd.
    imageFile = open(os.path.join('xkcd',
                                  '{0}-{1}'.format(os.path.basename(url),
                                            os.path.basename(comicUrl))),
                    'wb')

    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    count += 1
    if count == 10: break
    else:
        #Get the previous button's url.
        prevLink = soup.select('a[rel="prev"]')[0]
        url = 'https://xkcd.com' + prevLink.get('href')

print('Done.')