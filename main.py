# Author: HereIronman7746
# License: MIT
# Version: Alpha

import requests
from bs4 import BeautifulSoup
import os
import js2py
from clint.textui import progress

base = "https://vidembed.io"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
server = "https://mixdrop.co"
unpacker = requests.get("https://raw.githubusercontent.com/ParrotDevelopers/MixDrop_to_M3U/9198d12fc0ba93bd611ee56acd0695587a6ec695/compiler.js").text
# TODO: Add StreamSB support

def grab(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    iframe = soup.find('iframe')
    iframe_url = iframe['src'].replace("//", "https://")
    iframe_html = requests.get(iframe_url, headers=headers).text
    soup = BeautifulSoup(iframe_html, 'html.parser')
    links = soup.find_all('li', {'class': 'linkserver', 'data-status': '1'})
    for link in links:
        if server in link['data-video']:
            return link['data-video'].split('/e/')[1].split("?")[0]

def mixdrop(urlin):
    try:
        r = requests.get(server + "/e/" + urlin, headers=headers).text.replace('\n', '').split("return p}")[1].split("}))")[0] + "})"
        inputLink = "f" + r + ";"
        code = unpacker + inputLink
        videoURL = "https://" + js2py.eval_js(code).split('MDCore.wurl="//')[1].split('";')[0]
        return videoURL
    except:
        print("This video was removed or is unavailable")
        exit()

def main():
    print("Warning: This program is still in development and may not work properly")
    print("Search for a video in: ")
    print("1. Movies")
    print("2. Series")
    print("3. Exit")
    choice = input("Enter your choice: ")
    choice = int(choice)
    if choice == 1:
        movies()
    elif choice == 2:
        series()
    elif choice == 3:
        exit()

def series():
    print("Search for a series: ")
    os.system('cls')
    series = input("Enter the name of the series: ")
    url = f"{base}/search.html?keyword={series}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    links = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if 'season' in a['href'].split('-'):
                links.append(f"{base}{a['href']}")

    for i in range(len(names)):
        print(f"{i+1}. {names[i]}")
    choice = input("Enter your choice: ")
    choice = int(choice)
    os.system('cls')
    seriesurl = f"{links[choice-1]}"
    qv = seriesurl.split('/videos/')[1].split('-')[0]
    r = requests.get(seriesurl, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    os.system('cls')
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['alt'].lower():
            if qv in img.img['alt'].lower():
                names.append(img.img['alt'])
                images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if "/videos/" in a['href']:
            if qv in a['href']:
                links.append("https://vidembed.io" + a['href'])
    for i in range(len(names)):
        print(f"{i+1}. {names[i]}")
    choice = input("Enter your choice: ")
    choice = int(choice)
    urltoscrape = f"{links[choice-1]}"
    mp4url = mixdrop(grab(urltoscrape))
    print(f"Downloading {names[choice-1]}")
    r = requests.get(mp4url, stream=True)
    print(f"File size: {int(r.headers['Content-Length'])/1024/1024} MB")
    with open(f"{names[choice-1]}.mp4", "wb") as Pypdf:
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if ch:
                Pypdf.write(ch)
    print(f"{names[choice-1]} downloaded successfully")




def movies():
    print("Search for a movie: ")
    os.system('cls')
    movie = input("Enter the name of the movie: ")
    url = f"{base}/search.html?keyword={movie}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    links = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if not 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if not 'season' in a['href'].split('-'):
                links.append(f"{base}{a['href']}")

    for i in range(len(names)):
        print(f"{i+1}. {names[i]}")
    choice = input("Enter your choice: ")
    choice = int(choice)
    urltoscrape = f"{links[choice-1]}"
    mp4url = mixdrop(grab(urltoscrape))
    print(f"Downloading {names[choice-1]}")
    r = requests.get(mp4url, stream=True)
    print(f"File size: {int(r.headers['Content-Length'])/1024/1024} MB")
    with open(f"{names[choice-1]}.mp4", "wb") as Pypdf:
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if ch:
                Pypdf.write(ch)
    print(f"{names[choice-1]} downloaded successfully")
    

if __name__ == '__main__':
    main()

