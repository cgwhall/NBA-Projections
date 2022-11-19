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


##### Actually works, LFG!
def scrape_seasons(year_range):
    def empty_df(URL='https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats'):
        page = requests.get(URL)
        soup_obj = bs(page.content, 'lxml')
        table = soup_obj.find(id="per_game_stats")
        table_head = table.find('thead')
        header = table_head.find_all('th')
        categories = [header[cat]['aria-label'] for cat in range(len(header))]
        stats_df = pd.DataFrame(columns = categories[1:])
        stats_df['season'] = []
        return season_stats
    df = empty_df()
    for year in year_range:
        print(f'scraping {year}\'s stats')
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

# Create year range list
year_range=[*range(2018,2023)] #https://www.geeksforgeeks.org/range-to-a-list-in-python/
year_range


player_stats_df = scrape_seasons(year_range)







# Get URL
URL = "https://www.basketball-reference.com/leagues/NBA_2023_coaches.html#NBA_coaches"
page = requests.get(URL)

# print(page.text)

#Create Soup Object
soup = bs(page.content, "html.parser")
soup.prettify()

# Create table soup object
table_head= soup.find('thead')
table_head

header = table_head.find_all('th')
header[0]

categories = [header[cat]['aria-label'] for cat in range(len(header)) if len(header[cat]['aria-label']) > 0 if header[cat]['aria-label'] != '\xa0']
categories


##### Actually works, LFG!
def scrape_seasons(year_range):
    all_data = []
    for year in year_range:
        URL = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html#per_game_stats'
        page = requests.get(URL)
        time.sleep(5)
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
                all_data.append(cells)
        if year == 0:
            table = soup.find(id="per_game_stats")
            table_head = table.find('thead')
            header = table_head.find_all('th')
            categories = [header[cat]['aria-label'] for cat in range(len(header))]
            all_data.insert(0, categories)
        else:
            pass
        time.sleep(5)
    return all_data

path = '/Users/chandlerhall/Desktop/Github/NBA_Projections/NBA_Data.csv'
def save_to_csv(data, path):
    # Join and save to github folder
    lines = [','.join(line) for line in data]
    doc = '\n'.join(lines)
    with open(path, 'w') as ofile:
        ofile.write(doc)
        
player_stats_df = scrape_seasons(year_range)
        