#got a little bit of an optimization update
import discord
from config import settings
from discord import Client 
from discord.ext import commands

import requests
from bs4 import BeautifulSoup as BS

bot = commands.Bot(command_prefix = settings['prefix'])        

@bot.command()
async def watch(ctx, serial_str: str, decision: str): #input: !watch nameOfAShow films/series

    if decision == 'series' or decision == 'films': 
        r = requests.get(f"https://vhsbox.live/{decision}/")
        soup = BS(r.content,'lxml')
        
        async def lastPage(): # - getting the last page
            pagesList = []
            pagesList.append(soup.find('div', class_='navigation').text)
            pagesDiv = pagesList[0].split()
            lastPage = int(pagesDiv[-1])
            return lastPage
        
        serials = soup.find('div', class_ = 'content') # - all serials
        serialElements = serials.find_all('div', class_ = 'th-item') # - each serial info
        
        serialNames = [] # - list to fill with serial names
        for each in serialElements: # - searching for the desired serial on the first page
            serialNames.append(each.find('div', class_ = 'th-title nowrap').text)
        
        async def loop(currentPage):
            r1 = requests.get(f'https://vhsbox.live/{decision}/page/{currentPage}/')
            soup3 = BS(r1.content, 'lxml')
            
            serialsNext = soup3.find('div', class_ = 'content') # - all serials on 2+ pages
            serialElementsNext = serialsNext.find_all('div', class_ = 'th-item') # - each serial on 2+ pages
            
            serialNames.clear() 
            
            for eachNext in serialElementsNext:
                serialNames.append(eachNext.find('div', class_ = 'th-title nowrap').text)
                
            while serial_str not in serialNames:
                while currentPage <= await lastPage():
                    serialNames.clear()
                    for eachNext in serialElementsNext:
                        serialNames.append(eachNext.find('div', class_ = 'th-title nowrap').text)
                    return await loop(currentPage = currentPage + 1)
            
            for elNext in serialElementsNext:
                if serial_str == elNext.find('div', class_ = 'th-title nowrap').text:
                    url = elNext.find('a', {'class' : 'th-in'}).get('href')
                    #print(url)
                    
                    serialINFO = requests.get(url)
                    soup4 = BS(serialINFO.content, 'lxml')
                    
                    description = soup4.find('div', class_ = 'fdesc clr full-text clearfix').text
                    rating = soup4.find('div', class_ = 'frate frate-imdb').find('div', class_ = 'frate-count').text
                    release = soup4.find('div', class_ = 'fmeta fx-row fx-start').text
                    name = soup4.find('div', class_ = 'fright fx-1').find('h1').text
                    
                    allInfos = soup4.find('ul', class_ = 'flist')
                    eachInfosColumn = allInfos.find_all('li')
                    convToText = [x.text for x in eachInfosColumn]
                    textdiv = ' | '.join(convToText)
                    information = textdiv.split(' | ')
                    
                    genre = []
                    lastep = []
                    for element in information:
                        if 'Жанр' in element:
                            genre.append(element)
                        elif 'Добавлена' in element:
                            lastep.append(element)
                    
                    await ctx.send(name + '\n' + release + '\n' +  genre[0] + '\n' + description + '\n' + f'Рейтинг с IMDB: {rating}' + '\n' +  lastep[0])   
        if serial_str not in serialNames:
            await loop(2)
        else:
            for el in serialElements:
                name = el.find('div', class_ = 'th-title nowrap').text
                if serial_str == name:
                    url = el.find('a', {'class' : 'th-in'}).get('href')
                    #print(url)
                    
                    serialINFO = requests.get(url)
                    soup2 = BS(serialINFO.content, 'lxml')
                    
                    description = soup2.find('div', class_ = 'fdesc clr full-text clearfix').text
                    rating = soup2.find('div', class_ = 'frate frate-imdb').find('div', class_ = 'frate-count').text
                    release = soup2.find('div', class_ = 'fmeta fx-row fx-start').text
                    name = soup2.find('div', class_ = 'fright fx-1').find('h1').text
                    
                    allInfos = soup2.find('ul', class_ = 'flist')
                    eachInfosColumn = allInfos.find_all('li')
                    convToText = [x.text for x in eachInfosColumn]
                    textdiv = ' | '.join(convToText)
                    information = textdiv.split(' | ')
                    
                    genre = []
                    lastep = []
                    for element in information:
                        if 'Жанр' in element:
                            genre.append(element)
                        elif 'Добавлена' in element:
                            lastep.append(element)
                    
                    
                    await ctx.send(name + '\n' + release + '\n' +  genre[0] + '\n' + description + '\n' + f'Рейтинг с IMDB: {rating}' + '\n' + lastep[0])
    else: await ctx.send('Unknown command')


bot.run('OTc1NzY0NzY2NDEwODE3NTg2.GWtKRd.x0viJdlOQ6Gnor4kD-rEIF9xMAO_9Ewz77apWM')