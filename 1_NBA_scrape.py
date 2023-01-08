###################
# Web Scraping
##################

## Scrape tables from basket-reference.com to build datasets
    # 1. Scrape NBA players season stats for every season from 2002-2022
    # 2. Scrape NBA coaches for every season from 2002-2022
    # 3. Scrape NBA Players from only 2022 season to filter dataset later to only active players
    # 4. Save each as csv to Data folder

# Set Paths for save at end
absolute_path = '/Users/chandlerhall/Desktop/Github/'
players_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_players_data.csv'
coaches_path = f'{absolute_path}final-project-nba_prediction_modeling/DATA/NBA_coaches_data.csv'
act_players_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_active_players.csv'



import requests
from bs4 import BeautifulSoup as bs
import time

# Define Web Scraping Function
def scrape_nba(year_range, page=''):
    
    # Check end of url based on page arg
    end_url = page_dict[page]

    # Process each row for each year and append to all_data lists for csv save
    all_data = []
    for index, year in enumerate(year_range):
        URL = f'https://www.basketball-reference.com/leagues/NBA_{year}_{end_url}'
        page = requests.get(URL)
        soup = bs(page.content, 'lxml')
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 1: # skip empty rows in table
                pass
            else:
                cells=[stat.text.strip() for stat in cols]
                cells.append(str(year)) # add year of season
                
                if page != 'players': # for coaches page, insert coach name in postion 0
                    coach = row.find('th').text
                    cells.insert(0, coach)
                all_data.append(cells)
        if index == 0: # Use the first table to create the table header row and insert at top
            thead = soup.find('thead')
            tab = thead.find_all('tr')
            theads = tab[len(tab)-1].find_all('th')
            categories = [theads[cat]['data-stat'] for cat in range(len(theads))]
            categories.append('season')
            all_data.insert(0, categories)
        else:
            pass
        time.sleep(5) # Pause required by site for scraping
    def remove_dum(all_data): # Certain tables have formatted columns that contain no data, remove from final dataset
        dum_indices = [index for index, cell in enumerate(all_data[0]) if 'dum' in cell]
        for row in all_data:
            for col in sorted(dum_indices,reverse=True): #https://www.geeksforgeeks.org/python-remove-elements-at-indices-in-list/
                del row[col]
    remove_dum(all_data)
    return all_data

# Define save to csv function
def save_to_csv(data, path):
    # Join and save to github folder
    lines = [','.join(line) for line in data]
    doc = '\n'.join(lines)
    with open(path, 'w') as ofile:
        ofile.write(doc)
        
####################################
        
# Create year range list
year_range=[*range(2002,2023)] #https://www.geeksforgeeks.org/range-to-a-list-in-python/

# Define scrape dictionary
page_dict = {'players':'per_game.html#per_game_stats',
             'coaches': 'coaches.html#NBA_coaches'} # Can update dictionary to scrape any table
                                                    # from basketball-refernce site by changing url


# Scrape Seasons 2002 - 2022
players = scrape_nba(year_range, page='players')
coaches = scrape_nba(year_range, page='coaches')

# Scrape separate csv of only last season for active player match
## Used to filter out ex-players no longer in league from main dataframe
year_range=[2022]
act_players = scrape_nba(year_range, page='players')

# Save to CSVs in data folder
save_to_csv(players, players_path)
save_to_csv(coaches, coaches_path)
save_to_csv(act_players, act_players_path)

