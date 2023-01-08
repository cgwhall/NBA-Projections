####################
## DATA CLEANING
###################
    # 1. Treat duplicate observations from players who were traded mid-season
    # 2. Clean position assignments
    # 3. Filter dataset to include only players with significant sample size (minutes & games played)
    # 4. Filter dataset to only active players
    # 5. Add Variables
        # Years in the League
        # Year ^2
        # Player Efficiency
        # Cluster assignments
    # 6. Merge with Sentiment Scores
    # 7. Merge with Coaches

import pandas as pd

#Load Data File
absolute_path = '/Users/chandlerhall/Desktop/Github/' # Change to your path
data_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_players_data.csv'
act_players_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_active_players.csv'
coaches_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_coaches_data.csv'


players_df = pd.read_csv(data_path)


# Clean Column and Player Names
def clean_names(df):
    df = df.rename(str.lower, axis = 1)
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace(' ', '_')
    df.player = df.player.str.replace('*', '')
    return df

players_df = clean_names(players_df)



# For players who were traded mid-season and has two observations, take the total season stats observation and
# assign team with most amount of games played

# Define function to treat players traded mid-season
def traded_season(df):
    wdf = df
    for index, row in wdf.iterrows():
        
        # Take player's total season observation...
        if row['team_id'] == 'TOT':
            ply = row['player']
            ssn = row['season']
            year_tm = index
            
            # Look at next observations while in the same season (if traded multiple times) and find team most games
            # played for, assign that team name to total season observation and drop other observations
            index += 1
            games_played = []
            while wdf.loc[index]['season'] == ssn and wdf.loc[index]['player'] == ply:
                games_played.append(wdf.loc[index]['g'])
                index += 1
                if index == len(df):
                    break
            most_games = max(games_played)
            team = wdf.loc[(wdf.player == ply) & (wdf.season == ssn) & (wdf.g == most_games),'team_id'].tolist()
            wdf.at[year_tm, 'team_id'] = team[0]
    wdf = wdf.drop_duplicates(subset=['player', 'season'], keep='first')
    return wdf

players_df = traded_season(players_df)


## For players with multiple positions assigned...
## Replace with only first position
def pos_clean(x):
    if x[:2] == 'PG':
        return 'PG'
    if x[:2] == 'SG':
        return 'SG'
    if x[:2] == 'SF':
        return 'SF'
    if x[:2] == 'PF':
        return 'PF'
    if x[:1] == 'C':
        return 'C'

players_df['pos'] = players_df['pos'].map(pos_clean)


### FILTER DATA ###

# Remove players that don't play significant games/minutes
players_df = players_df[(players_df['mp_per_g'] >=10) & (players_df['g'] >= 10)]


# Only Active Players
active_players = pd.read_csv(act_players_path)
active_lst = list(active_players['player'].unique())

players_df = players_df[players_df['player'].isin(active_lst)]



### ADD VARIABLES ###

# Years in the League
# For each observation, attribute how many years in the league that player has played
def years_in_league(df):
    wdf = df
    # prepare df to iterate through each player in the correct season order
    wdf = wdf.sort_values(['player','season']).reset_index(drop=True)
    wdf['year'] = 0 # create variable for years in league
    
    # Assign index position to years_played and attribute to each player
    for index in range(len(wdf)):
        if wdf.loc[index]['year'] == 0:
            years_played = 1
            player = wdf.loc[index]['player']
            wdf.at[index, 'year'] = years_played
            index += 1
            if index == len(wdf):
                break     
            while wdf.loc[index]['player'] == player:
                years_played += 1
                wdf.at[index, 'year'] = years_played
                index += 1
                if index == len(wdf):
                    break
        else:
            pass
    return wdf

players_df = years_in_league(players_df)

## Add Year^2
players_df['year2'] = players_df['year'].apply(lambda x: x**2)



# Add player efficiency scores
players_df['player_efficiency'] = ((players_df['pts_per_g'] + players_df['trb_per_g'] + 
                                    players_df['ast_per_g'] + players_df['stl_per_g'] + 
                                    players_df['blk_per_g']) - 
                                   (players_df['fga_per_g'] + 
                                    players_df['fg_per_g']) + 
                                   (players_df['fta_per_g'] - 
                                    players_df['ft_per_g']) + 
                                    players_df['tov_per_g'])


# Define Clustering Function
def cluster(df, cats):
    for cat in cats:
        col_name = cat+'_per_min'
        df[col_name] = df[cats[cat]]/df['mp_per_g']
        
        # Find each player's best season, cluster by decile rank
        players_max = df.groupby('player').max(col_name).reset_index()
        players_max['decile'] = pd.qcut(players_max[col_name], 20, labels = False) #https://www.geeksforgeeks.org/quantile-and-decile-rank-of-a-column-in-pandas-python/

        # Create dictionary to attribute
        pts_dict = dict(zip(players_max.player, players_max.decile))

        # Get category cluster from dictionary
        cluster_name = cat+'_cluster'
        df[cluster_name] = df["player"].apply(lambda x: pts_dict.get(x)) #https://stackoverflow.com/questions/51881503/assign-a-dictionary-value-to-a-dataframe-column-based-on-dictionary-key
    return df


# Stats to cluster by
categories = {'reb':'trb_per_g', 'assists':'ast_per_g', 'pts':'pts_per_g'}


# Cluster by selected categories
players_df = cluster(players_df, categories)


### Merge DFs
# Merge with Coaches
coaches_df = pd.read_csv(coaches_path)

# Reduce df to variables of interest
coaches_df = coaches_df[['coach', 'team', 'season', 'car_wpct']]

# Merge with complete data frame
players_df = players_df.merge(coaches_df, left_on=['team_id', 'season'], right_on=['team', 'season'])



## SAVE TO CSV
save_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_cleaned_data.csv'

from pathlib import Path  
filepath = Path(save_path)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
players_df.to_csv(filepath) 





