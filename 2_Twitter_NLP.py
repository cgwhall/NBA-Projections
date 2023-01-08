#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 17:00:52 2022

@author: nicholassimon
"""


# Import relevant libraries
import spacy
import pandas as pd
from spacytextblob.spacytextblob import SpacyTextBlob
import snscrape.modules.twitter as sntwitter
import statistics
import os



# NLP variables
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')



# Import data
absolute_path = '/Users/nicholassimon/Documents/GitHub/' # Change to your path
data_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_players_data.csv'
nba_df = pd.read_csv(data_path)



# Create list of twitter handles
# https://fansided.com/2018/10/11/nba-twitter-beat-writers/
handles = ['ByJayKing','APOOCH', 'StevePopper','PompeyOnSixers', 'JLew1050', 'KCJHoop', 
           'CavsJoeG', 'detnewsRodBeard','ScottAgness', 'Matt_Velazquez', 'CVivlamoreAJC', 
           'rick_bonnell', 'IraHeatBeat', 'JoshuaBRobbins', 'CandaceDBuckner', 'chrisadempsey', 
           'JerryZgoda', 'royceyoung', 'mikegrich', 'Andyblarsen', 'AnthonyVslater',
           'DanWoikeSports', 'Mike_Bresnahan', 'GeraldBourguet', 'mr_jasonjones', 'MFollowill', 
           'Jonathan_Feigen', 'MyMikeCheck', 'Jim_Eichenhofer', 'JeffGSpursZone']



# Create function that scrapes Twitter and calculates sentiment scores
def scrape_sentiment(nba_df, handles):
    
    # Create a list of players
    player_list = list(set(nba_df['player']))
    
    # Create a list of years and a dictionary in which the years serve as keys
    year_range=[*range(2009,2023)]
    year_dict = {year: [] for year in year_range}
    
    # Create a dicionary in which years serve as keys and handles serve as values 
    # https://stackoverflow.com/questions/20585920/how-to-add-multiple-values-to-a-dictionary-key
    handles_dict = {}
    for key, val in year_dict.items():
        for handle in handles:
            handles_dict.setdefault(key, []).append(handle)
    
    # Scrape Twitter and store tweets in a df
    # https://www.youtube.com/watch?v=jtIMnmbnOFo
    # https://www.youtube.com/watch?v=uPKnSq6TaAk
    # https://stackoverflow.com/questions/53509168/extract-year-month-and-day-from-datetime64ns-utc-python
    tweets = []
    for year, handles in handles_dict.items():
        for handle in handles:
            query = f'(from:{handle}) until:{year}-10-15 since:{year}-09-01'
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                tweets.append([tweet.date, tweet.username, tweet.content])
    tweets_df = pd.DataFrame(tweets, columns=['Date', 'Handle', 'Tweet'])
    datetimes = pd.to_datetime(tweets_df['Date'])
    tweets_df['Season'] = datetimes.dt.year
    
    # Determine sentiment scores for all tweets in the df
    # https://www.edureka.co/community/43215/how-to-find-the-index-of-a-particular-value-in-a-dataframe
    # https://stackoverflow.com/questions/1966207/convert-numpy-array-to-python-list
    score_list = []
    tweets = tweets_df['Tweet']
    for player in player_list:
        for tweet in tweets:
            if player in tweet:
                doc = nlp(tweet)
                pol_score = round(doc._.blob.polarity, 4)
                index_no = tweets_df[tweets_df['Tweet']==tweet].index.values
                index_no = index_no.astype(int)[0]
                date_list = list(tweets_df['Season'])
                season = date_list[index_no]
                score_list.append([player, pol_score, season])
                
    # Create a df in which average sentiment scores for each player during a given year are stored 
    score_list
    headers = ['player', 'sentiment_score', 'season']
    sentiment_df = pd.DataFrame(score_list, columns=headers)
    sentiment_df = sentiment_df.groupby(['player', 'season']).mean().reset_index()
    
    # Merge sentiment_df with nba_df
    nba_df = nba_df.merge(sentiment_df, on=['player', 'season'], how='left')
    nba_df['sentiment_score'].fillna(0, inplace = True)
    return nba_df



# Update nba_df using the scrape_sentiment function
nba_df = scrape_sentiment(nba_df, handles) 



# Save the updated version of nba_df as a csv
nba_df.to_csv(data_path)



