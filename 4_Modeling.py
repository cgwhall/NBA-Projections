###########################
## Prediction Modeling
##########################


import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

#Load Data File
absolute_path = '/Users/chandlerhall/Desktop/Github/' # Change to your path
data_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/NBA_cleaned_data.csv'

players_df = pd.read_csv(data_path)


# Data Transformations
players_df = players_df.astype({'pts_cluster':'str', 'assists_cluster':'str', 'reb_cluster':'str'})

# Define Stats of Interest
stats = ['pts', 'assists', 'reb']

# For each model, run regression and return coefficients
def return_predictions(df, stat, model_formula=''):
    model = smf.ols(f'{model_formula}', data = df)
    results = model.fit()
    rs = results.params
    return rs


## MODEL 1 Simple OLS
def predict_simple(df, stats):
    for stat in stats:
        formula = f'{stat}_per_min ~ year + year2'
        rs = return_predictions(df, stat, formula)
        prediction = []
        for index, player in df.iterrows():
            nxt_year = rs[0] + (rs[1]*(df.loc[index]['year']+1)) + rs[2]*((df.loc[index]['year']+1)**2)
            prediction.append(nxt_year)
        df[f'{stat}_prediction_mod1'] = prediction
    return df

players_df = predict_simple(players_df, stats)

## MODEL 2 Clustering
def predict_cluster(df, stats):
    for stat in stats:
        formula = f'{stat}_per_min ~ year + year2 + {stat}_cluster'
        rs = return_predictions(df, stat, formula)
        prediction = []
        for index, player in df.iterrows():
            cluster = df.loc[index][f'{stat}_cluster']
            cluster = f'{stat}_cluster[T.'+cluster+']'
            
            if cluster != f'{stat}_cluster[T.0]':
                nxt_year = df.loc[index][f'{stat}_per_min']
                + (rs[20]*(df.loc[index]['year']+1))
                + rs[21]*((df.loc[index]['year']+1)**2)
                + rs[cluster]
                prediction.append(nxt_year)
            else:
                nxt_year = df.loc[index][f'{stat}_per_min']
                + (rs[20]*(df.loc[index]['year']+1))
                + rs[21]*((df.loc[index]['year']+1)**2)
                prediction.append(nxt_year)
        df[f'{stat}_prediction_mod2'] = prediction
    return df
        
players_df = predict_cluster(players_df, stats)


## MODEL 4 Player Fixed Effects
def predict_player_model(df, stats):
    for stat in stats:
        prediction = []
        for index, row in df.iterrows():
            player = df.loc[index]['player']
            wdf = df[df['player'] == player]
            if len(wdf) >= 3:
                model = smf.ols(f'{stat}_per_min ~ year + year2', data = wdf)
                results = model.fit()
                rs = results.params
                nxt_year = rs[0] + (rs[1]*(wdf.loc[index]['year']+1)) + rs[2]*((wdf.loc[index]['year']+1)**2)
                prediction.append(nxt_year)
            else:
                prediction.append(np.nan)
        df[f'{stat}_prediction_mod3'] = prediction 
    return df

players_df = predict_player_model(players_df, stats)


# Model 4 Player Fixed Effects w/ Controls
def predict_player_model_controls(df, stats):
    for stat in stats:
        prediction = []
        for index, row in df.iterrows():
            player = df.loc[index]['player']
            wdf = df[df['player'] == player]
            if len(wdf) >= 3:
                model = smf.ols(f'{stat}_per_min ~ year + year2 + sentiment_score + car_wpct', data = wdf)
                results = model.fit()
                rs = results.params
                nxt_year = rs[0] + (rs[1]*(wdf.loc[index]['year']+1)) 
                + rs[2]*((wdf.loc[index]['year']+1)**2)
                + rs[3]*wdf.loc[index]['sentiment_score']
                + rs[4]*wdf.loc[index]['car_wpct']
                prediction.append(nxt_year)
            else:
                prediction.append(np.nan)
        df[f'{stat}_prediction_mod4'] = prediction 
    return df


players_df = predict_player_model_controls(players_df, stats)


## SAVE TO CSV
save_path = f'{absolute_path}final-project-nba_prediction_modeling/Data/all_data.csv'

from pathlib import Path  
filepath = Path(save_path)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
players_df.to_csv(filepath) 
