#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:13:27 2022

@author: chandlerhall
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# Get URL
URL = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats"
page = requests.get(URL)

# print(page.text)

#Create Soup Object
soup = bs(page.content, "html.parser")


# Create table soup object
table = soup.find(id="per_game_stats")

## Scrape table header row
table_head = table.find('thead')
header = table_head.find_all('th')

categories = [header[cat]['aria-label'] for cat in range(len(header))]

season_stats = pd.DataFrame(columns = categories[1:]) 

## Scrape table rows
tbody = soup.find('tbody')
rows = tbody.find_all('tr') 
for row in rows:
    cols=row.find_all('td')
    if len(cols) < 1:
        pass
    else:
        cols=[stat.text.strip() for stat in cols]  # https://datascience.stackexchange.com/questions/10857/how-to-scrape-a-table-from-a-webpage
        season_stats.loc[len(season_stats)] = cols
        print(cols)


len(season_stats.columns)

# AUTOMATED

year_range=[*range(2018,2023)] #https://www.geeksforgeeks.org/range-to-a-list-in-python/
year_range

# def start_df(URL):
#     URL = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats'
#     page = requests.get(URL)
#     soup = bs(page.content, 'lxml')
#     table = soup.find(id="per_game_stats")
#     table_head = table.find('thead')
#     header = table_head.find_all('th')
#     categories = [header[cat]['aria-label'] for cat in range(len(header))]
#     season_stats = pd.DataFrame(columns = categories[1:])
#     season_stats['season'] = []
#     return season_stats

# df = start_df(season_stats)


##### Actually works, LFG!
def scrape_seasons(year_range):
    def start_df(URL='https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats'):
        page = requests.get(URL)
        soup = bs(page.content, 'lxml')
        table = soup.find(id="per_game_stats")
        table_head = table.find('thead')
        header = table_head.find_all('th')
        categories = [header[cat]['aria-label'] for cat in range(len(header))]
        season_stats = pd.DataFrame(columns = categories[1:])
        season_stats['season'] = []
        return season_stats
    df = start_df()
    for year in year_range:
        print(f'time for {year}\'s stats')
        URL = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html#per_game_stats'
        page = requests.get(URL)
        time.sleep(5)
        print('it\'s a waiting game....')
        soup = bs(page.content, 'lxml')
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 1:
                pass
            else:
                cells=[stat.text.strip() for stat in cols]
                cells.append(year)
                season_stats = df
                season_stats.loc[len(season_stats)] = cells
        pd.concat([df, season_stats])
        print(f'{year} stats scraped and added!')
    return season_stats

df = scrape_seasons(year_range)


