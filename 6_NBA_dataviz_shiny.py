# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 14:20:06 2022

@author: nicol
"""
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive


## Uploading Data
my_path = r'C:\Users\nicol\OneDrive - The University of Chicago\Desktop\final-project-nba_prediction_modeling\Data'
fname1 = 'all_data.csv'

## Setting the data
df = pd.read_csv(os.path.join(my_path, fname1))
df['error1_pts'] = df['pts_prediction_mod1'] - df['pts_per_min']

var_dict = {'Points':'pts_per_min',
            'Rebounds':'reb_per_min',
            'Assists':'assists_per_min'}

df.sample(n=20)

var_dict1 = {j:i for i, j in var_dict.items()}

df_season = df.groupby('player')['year'].sum().reset_index()
season_check = {player:nseasons for (player, nseasons) in zip(df_season['player'], df_season['year'])}

players_dict = {player:player for (player, nseasons) in season_check.items() if nseasons > 1}

models_dict = {'pts_prediction_mod1':'Cluster Fixed Effects' ,
               'pts_prediction_mod2':'Player Fixed Effects',
               'pts_prediction_mod3':'No Fixed Effects with Twitter Sentiment Analysis' ,
               'pts_prediction_mod4':'Cluster Fixed Effects with Twitter Sentiment Analysis'}

logo = 'https://andscape.com/wp-content/uploads/2017/06/nbalogo.jpg?w=1400'

## Shiny
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav('Stactic Productivity',
               ui.row(
                   ui.column(1),
                   ui.column(3, ui.img(src=logo, height=150, width=230)),
                   ui.column(4, ui.panel_title('NBA Players Productivity'),
                             ui.hr()
                             ),
                   ui.column(1),
                   ui.column(3, ui.input_select('x1', 'Select Productivity Category', var_dict1),
                             ui.input_select('x2', 'Select Players', players_dict))
                   ),
               ui.row(
                   ui.output_plot('prod_plot')
                   )
               ),
    
        ui.nav('Productivity Comparison',
               ui.row(
                   ui.column(1),
                   ui.column(3, ui.img(src=logo, height=150, width=230)),
                   ui.column(4, ui.panel_title('NBA Players Comparison'),
                             ui.hr()
                             ),
                   ui.column(1),
                   ui.column(3, ui.input_select('x3', 'Select Productivity Category', var_dict1),
                             ui.input_select('x4', 'Select Player 1', players_dict),
                             ui.input_select('x5', 'Select Player 2', players_dict))
                   ),
               
               ui.row(ui.output_plot('comparison_plot'))                                             
        ),
        
        ui.nav('Productity Predictions - 2022',
               ui.row(
                   ui.column(1),
                   ui.column(3, ui.img(src=logo, height=150, width=230)),
                   ui.column(4, ui.panel_title("NBA Players' Productivity Prediction for 2022"),
                             ui.hr()
                             ),
                   ui.column(1),
                   ui.column(3,
                             ui.input_select('x8',
                                             'Select Model',
                                             models_dict),
                             ui.input_select('x6',
                                             'Select Sample',
                                             {'top':'Top 20 Players' , 'random':'Random Sample of 20 Players'}),
                             ui.input_slider('x7', 
                                             'Choose a sample size:',
                                             5, 20, 1)
                             )
                   ),
               
               ui.row(ui.output_plot('predict_plot'))
            )
   )
)

def server(input, output, session):
    @reactive.Calc
    def get_dataset():
        df1 = df[df['player'].isin([input.x2()])]
        return df1
    
    @reactive.Calc
    def get_dataset1():
        df1 = df[df['player'].isin([input.x4(), input.x5()])]
        return df1
    
    @reactive.Calc
    def get_dataset2():
        df1 = df[df['season']==2022]
        df1['error1_pts'] = df[input.x8()] - df['pts_per_min']

        if input.x6() == 'top':
            df1 = df1.sort_values(by='pts_per_min', ascending=False).head(input.x7())            
        else:
            df1 = df1.sample(n=input.x7())
            
        
            
        return df1
    
    @output
    @render.plot
    def prod_plot():
        df1 = get_dataset()
        sns.set_style("darkgrid")
        sns.despine()
        ax = sns.lineplot(data=df1, 
                          x='year', 
                          y=input.x1(), 
                          hue='player',
                          legend=False)
        plt.title(f"Average {var_dict1[input.x1()]} throughout {input.x2()}'s career")
        plt.ylabel(f'Average {var_dict1[input.x1()]} per minute')
        plt.xlabel('Season')
        ax.set_xticks(range(1, df1['year'].max()+1))
        
        return ax
    
    @output
    @render.plot
    def comparison_plot():
        df1 = get_dataset1()
        ax = sns.lineplot(data=df1, 
                          x='year', 
                          y=input.x3(), 
                          hue='player', 
                          legend=False)
        plt.title(f"Average {var_dict1[input.x3()]} comparison of {input.x4()} and {input.x5()}")
        plt.ylabel(f'Average {var_dict1[input.x3()]} per minute')
        plt.xlabel('Season')
        ax.set_xticks(range(1, df1['year'].max()+1))
        
    @output
    @render.plot
    def predict_plot():
        df2 = get_dataset2()
        
        sns \
            .scatterplot(data=df2, 
                          x='error1_pts', 
                          y='player',
                          hue='error1_pts',
                          palette='PuOr_r',
                          edgecolor='black',
                          legend=False) \
            .set(title=f'Errors for the {models_dict[input.x8()]} 2022 Predictions',
                 xlabel='Errors',
                 ylabel='Players')
        plt.axvline(x=0, color='Red', lw=1).set_linestyle("--")
        plt.xlim(-0.5, 0.5)

app = App(app_ui, server)
            
