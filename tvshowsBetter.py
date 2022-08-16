from cgitb import text
from turtle import up
import requests
from bs4 import BeautifulSoup as BS

r = requests.get("https://hdi.zetfix.online/serials/")
soup = BS(r.content,'lxml')

# - finding number of the last page
listOfPages = soup.find('div', id = 'bottom-nav')
lastPageClass = listOfPages.find('div', class_ = 'bottom-nav clr ignore-select')
listofPagesSingle = []
listofPagesSingle.append(lastPageClass.find('div', class_ = 'navigation').text)
listofPages = listofPagesSingle[0].split()
lastPage = int(listofPages[-1])


serial_str = str(input())

serials = soup.find("div", class_ = 'cont center')
serialsCode = serials.find_all("div", class_ = 'vi-desc')

serialName = [] # - list to fill with serial names
for serial in serialsCode: # - searching for serials name on the first page / r&soup refers to the first one
    serialName.append(serial.find("div", class_ = 'vi-title').text)

def loop(currentPage): 
    
    r1 = requests.get(f"https://hd.zetfix.online/serials/page/{currentPage}/")
    soup3 = BS(r1.content, 'html.parser')
     
    serialsNext = soup3.find("div", class_ = 'cont center')
    serialsCodeNext = serialsNext.find_all("div", class_ = 'vi-desc')
    
    serialName.clear() # - clearing info of the first page
    
    for serialNext in serialsCodeNext:
        serialName.append(serialNext.find("div", class_ = 'vi-title').text) # - getting info of the second page
    
    #if input isnt found on second page, goes searching on next pages
    while serial_str not in serialName:
        while currentPage <= lastPage:
            serialName.clear()
            for serialNext in serialsCodeNext:
                serialName.append(serialNext.find("div", class_ = 'vi-title').text)
            return loop(currentPage = currentPage + 1)

    z = soup3.find_all("div", class_ = "video-item with-mask new-item")
    for i in z:
       alt = i.find('a', class_ = 'vi-img img-resp-h')
       img = alt.find('img', alt = True)
       if serial_str == img['alt']:
           a_href = i.find("a", {"class":"vi-img img-resp-h"}).get("href") #url of the serial
           print(a_href)
           
           serialINFO = requests.get(a_href)
           soup4 = BS(serialINFO.content, 'html.parser')
           
           description = soup4.find("div", id = "serial-kratko")
           print(description.text)
           rating = soup4.find('div', class_ = 'mediablock')
           accRating = rating.find('span', class_ = 'rat-imdb')
           print('Рейтинг с IMDB ' + accRating.text)
  

if serial_str not in serialName:
    loop(2) # - going to scan the second page and continiously all the pages if input isnt found
else: # - getting info of the serial
    z = soup.find_all("div", class_ = "video-item with-mask new-item") # - classes of all serials
    for i in z:
       alt = i.find('a', class_ = 'vi-img img-resp-h')
       img = alt.find('img', alt = True) # - getting titles of serials
       if serial_str == img['alt']:
           a_href = i.find("a", {"class":"vi-img img-resp-h"}).get("href") # - link to the desired serial
           
           serialINFO = requests.get(a_href)
           soup2 = BS(serialINFO.content, 'lxml')

           description = soup2.find('div', id='serial-kratko')
           
           print(serialINFO.content)
           #rating = soup2.find('div', class_ = 'mediablock')
           #accRating = rating.find('span', class_ = 'rat-imdb')
           #print(description.text)
           #print('Рейтинг с IMDB' + accRating.text)
